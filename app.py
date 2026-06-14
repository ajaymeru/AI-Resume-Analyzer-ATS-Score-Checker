import streamlit as st
import plotly.graph_objects as go
from pdf_parser import extract_text_from_pdf
from analyzer import analyze_resume, PREDEFINED_SKILLS
from report_generator import generate_pdf_report
import re

# Set page configurations
st.set_page_config(
    page_title="AI Resume Analyzer & ATS Score Checker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# Premium Styling & CSS Injections
# ----------------------------------------------------

# Custom CSS for modern glassmorphism UI & custom typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Global Typography overrides */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Professional Gradient Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 2.5rem 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    .hero-banner h1 {
        font-size: 2.6rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        color: #E2E8F0;
    }
    .hero-banner p {
        font-size: 1.1rem;
        font-weight: 300;
        color: #CBD5E0;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    

    
    /* Styled tag pills */
    .tag-pill {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        font-size: 0.88rem;
        font-weight: 500;
        border-radius: 50px;
        transition: all 0.2s;
    }
    .tag-pill-match {
        background-color: #E6FFFA;
        color: #0F5132;
        border: 1px solid #BADBCC;
    }
    .tag-pill-match:hover {
        background-color: #D1E7DD;
    }
    .tag-pill-missing {
        background-color: #FFF5F5;
        color: #842029;
        border: 1px solid #F8D7DA;
    }
    .tag-pill-missing:hover {
        background-color: #F8D7DA;
    }
    .tag-pill-additional {
        background-color: #EBF8FF;
        color: #084298;
        border: 1px solid #B6D4FE;
    }
    .tag-pill-additional:hover {
        background-color: #CFE2FF;
    }
    
    /* Stats Numbers */
    .stat-number {
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1;
        margin-top: 5px;
    }
    .stat-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #718096;
        font-weight: 600;
    }
    
    /* Custom divider line */
    .divider {
        height: 1px;
        background-color: #E2E8F0;
        margin: 1.5rem 0;
    }
    
    /* Dark Mode overrides if simulated */
    .dark-mode-container {
        background-color: #1A202C !important;
        color: #EDF2F7 !important;
        border-color: #2D3748 !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Predefined Sample Data
# ----------------------------------------------------
SAMPLE_JDS = {
    "Select a Sample Job Description": "",
    "Full-Stack Software Engineer": """Requirements:
- Strong experience with Python, JavaScript, and React.
- Hands-on experience with Node.js and REST APIs.
- Familiarity with SQL databases (PostgreSQL/MySQL) and MongoDB.
- Solid understanding of Git version control.
- Experience with DevOps practices, Docker, and AWS cloud deployment.
- Understanding of Agile methodologies and CI/CD pipelines.""",
    "Data Scientist / ML Engineer": """Requirements:
- Proficient in Python programming.
- Solid experience in Machine Learning, Data Analysis, and statistical modeling.
- Hands-on experience with Pandas, NumPy, Scikit-learn, and PyTorch or TensorFlow.
- Experience building dashboards using Power BI or Tableau.
- Proficiency in SQL for querying and database management.
- Strong Git skills and experience developing in Linux environments.""",
    "Product / Project Manager": """Requirements:
- Excellent communication and leadership skills.
- Proven track record managing software development life cycle (SDLC).
- Experience working with Jira, Confluence, and Agile frameworks.
- Familiarity with SQL for basic data querying and Data Analysis.
- High proficiency in Excel for reporting and metrics tracking.
- Experience with cloud computing concepts (AWS/Azure)."""
}


# ----------------------------------------------------
# HTML Keyword Highlighter Helper
# ----------------------------------------------------
def highlight_keywords_in_html(text: str, keywords: list) -> str:
    import html
    html_text = html.escape(text)
    html_text = html_text.replace("\n", "<br/>")
    
    # Sort keywords by length descending to match longer multi-word phrases first
    sorted_keywords = sorted(list(set(keywords)), key=len, reverse=True)
    
    for word in sorted_keywords:
        if not word.strip():
            continue
        # Use regex to find and replace with case-insensitivity, preserving original casing!
        # Wrap matching words in a styled mark tag while avoiding matching inside already created tags
        pattern = r'(<[^>]+>)|(?<![a-zA-Z0-9_])(' + re.escape(word) + r')(?![a-zA-Z0-9_])'
        
        def repl(match):
            if match.group(1):
                return match.group(1)
            val = match.group(2)
            return f'<mark style="background-color: #B2F5EA; color: #234E52; border-radius: 4px; padding: 1px 4px; font-weight: 500;">{val}</mark>'
            
        html_text = re.sub(pattern, repl, html_text, flags=re.IGNORECASE)
    return html_text

# ----------------------------------------------------
# Main Layout Construction
# ----------------------------------------------------

# Hero Header Banner
st.markdown("""
<div class="hero-banner">
    <h1>AI Resume Analyzer & ATS Score Checker</h1>
    <p>Upload your resume, paste the job description, and get instant NLP-powered ATS optimization metrics & feedback.</p>
</div>
""", unsafe_allow_html=True)

# Main columns
col_inputs, col_dash = st.columns([1, 1.3])

with col_inputs:
    st.subheader("📋 Step 1: Input Job Description")
    
    # Option to select a pre-made JD
    selected_sample_jd = st.selectbox(
        "Try a Predefined Sample Job Description:",
        options=list(SAMPLE_JDS.keys())
    )
    
    default_jd_text = SAMPLE_JDS[selected_sample_jd] if selected_sample_jd != "Select a Sample Job Description" else ""
    
    jd_input = st.text_area(
        "Paste the Target Job Description:",
        value=default_jd_text,
        height=180,
        placeholder="Requirements:\n- Strong knowledge of Python...\n- Familiarity with SQL and AWS..."
    )
    
    st.subheader("📄 Step 2: Upload Resume")
    
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF format only):",
        type=["pdf"]
    )
    
    resume_text = ""
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting text from PDF..."):
                resume_text = extract_text_from_pdf(uploaded_file)
            st.success("Successfully extracted text from uploaded PDF!")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    
    # Trigger button
    analyze_clicked = st.button("🚀 Analyze Resume Compatibility", use_container_width=True, type="primary")

with col_dash:
    if analyze_clicked:
        if not resume_text:
            st.warning("⚠️ Please upload a PDF resume to begin.")
        elif not jd_input.strip():
            st.warning("⚠️ Please paste a job description to analyze against.")
        else:
            with st.spinner("Evaluating ATS score & processing skills list..."):
                # Run NLP calculations
                analysis = analyze_resume(resume_text, jd_input)
                
            # Store calculations in session state to persist between downloads
            st.session_state["analysis"] = analysis
            st.session_state["resume_text"] = resume_text
            st.session_state["jd_input"] = jd_input
            
    # Check if analysis results are in state
    if "analysis" in st.session_state:
        analysis = st.session_state["analysis"]
        res_text = st.session_state["resume_text"]
        jd_txt = st.session_state["jd_input"]
        
        score = analysis["ats_score"]
        strength = analysis["strength_level"]
        
        # Color indicator mapping
        color_map = {
            "Excellent": "#2F855A", # Green
            "Good": "#2B6CB0",      # Blue
            "Average": "#D69E2E",   # Orange
            "Weak": "#C53030"       # Red
        }
        badge_color = color_map.get(strength, "#718096")
        
        # ----------------------------------------------------
        # Dashboard Panel
        # ----------------------------------------------------
        
        # 1. Executive Summary Metrics
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        
        with m_col1:
            st.metric(label="ATS Score", value=f"{score}%")
            
        with m_col2:
            st.metric(label="Strength", value=strength)
            
        with m_col3:
            st.metric(label="Word Count", value=analysis["word_count"])
            
        with m_col4:
            st.metric(label="Read Time", value=f"{analysis['reading_time']} min")
            
        # 2. Charts Section
        st.subheader("📊 Analytical Metrics Visualizations")
        c_col1, c_col2 = st.columns(2)
        
        with c_col1:
            # Gauge Chart
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "ATS Matching Level", 'font': {'size': 18, 'color': '#2D3748', 'family': 'Outfit'}},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#718096"},
                    'bar': {'color': '#1A365D'},
                    'bgcolor': "white",
                    'borderwidth': 1,
                    'bordercolor': "#CBD5E0",
                    'steps': [
                        {'range': [0, 40], 'color': '#FED7D7'},
                        {'range': [40, 70], 'color': '#FEEBC8'},
                        {'range': [70, 85], 'color': '#EBF8FF'},
                        {'range': [85, 100], 'color': '#C6F6D5'}
                    ],
                }
            ))
            fig_gauge.update_layout(height=240, margin=dict(l=30, r=30, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        with c_col2:
            # Pie Chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Matching Skills', 'Missing Skills', 'Other Skills'],
                values=[len(analysis["matching_skills"]), len(analysis["missing_skills"]), len(analysis["additional_skills"])],
                hole=.45,
                marker=dict(colors=['#48BB78', '#E53E3E', '#4299E1']),
                textinfo='value+percent',
                textfont=dict(size=12, family='Outfit')
            )])
            fig_pie.update_layout(
                title=dict(text="Skills Breakdown Comparison", font=dict(size=18, color='#2D3748', family='Outfit'), x=0.5, xanchor='center'),
                height=240, 
                margin=dict(l=20, r=20, t=50, b=20), 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        # 3. Bar Chart for Missing Keywords Frequency
        if analysis["missing_keywords"]:
            counts = []
            valid_kw = []
            for kw in analysis["missing_keywords"][:8]:
                cnt = len(re.findall(r'\b' + re.escape(kw) + r'\b', jd_txt.lower()))
                if cnt > 0:
                    counts.append(cnt)
                    valid_kw.append(kw)
            
            if counts:
                fig_bar = go.Figure(go.Bar(
                    x=counts,
                    y=valid_kw,
                    orientation='h',
                    marker_color='#E53E3E',
                    text=counts,
                    textposition='auto',
                ))
                fig_bar.update_layout(
                    title=dict(text="Top Missing Keywords (Frequency in JD)", font=dict(size=18, color='#2D3748', family='Outfit'), x=0.5, xanchor='center'),
                    yaxis=dict(autorange="reversed", tickfont=dict(size=12, family='Outfit')),
                    xaxis=dict(title="Occurrences in Job Description", tickfont=dict(size=11, family='Outfit')),
                    height=240,
                    margin=dict(l=20, r=20, t=50, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
        # 4. Contact Information Scan Results
        st.subheader("🔍 Contact Details Scan")
        cc1, cc2, cc3, cc4 = st.columns(4)
        
        contact = analysis["contact_info"]
        def display_contact_status(label: str, found: bool):
            icon = "✅" if found else "❌"
            status_text = "Found" if found else "Missing"
            color = "#2F855A" if found else "#C53030"
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 8px; border: 1px solid #E2E8F0; text-align: center; background-color: #F7FAFC;">
                <span style="font-size: 1.2rem;">{icon}</span><br/>
                <span style="font-size: 0.8rem; color: #718096; font-weight: 500;">{label}</span><br/>
                <span style="font-weight: 600; color: {color};">{status_text}</span>
            </div>
            """, unsafe_allow_html=True)
            
        with cc1:
            display_contact_status("Email", contact["email"])
        with cc2:
            display_contact_status("Phone Number", contact["phone"])
        with cc3:
            display_contact_status("LinkedIn", contact["linkedin"])
        with cc4:
            display_contact_status("GitHub", contact["github"])
            
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
        # 5. Skill Pills Display
        st.subheader("🛠️ Detailed Skills Mapping")
        
        tab_matching, tab_missing, tab_additional = st.tabs([
            f"Matching Skills ({len(analysis['matching_skills'])})", 
            f"Missing Required Skills ({len(analysis['missing_skills'])})", 
            f"Other Resume Skills ({len(analysis['additional_skills'])})"
        ])
        
        with tab_matching:
            if analysis["matching_skills"]:
                for s in analysis["matching_skills"]:
                    st.markdown(f'<span class="tag-pill tag-pill-match">✔ {s}</span>', unsafe_allow_html=True)
            else:
                st.info("No matching skills found. Try aligning keywords to the JD.")
                
        with tab_missing:
            if analysis["missing_skills"]:
                st.markdown("<p style='color: #718096; font-size: 0.9rem;'>These skills were found in the Job Description but are missing in your resume:</p>", unsafe_allow_html=True)
                for s in analysis["missing_skills"]:
                    st.markdown(f'<span class="tag-pill tag-pill-missing">✖ {s}</span>', unsafe_allow_html=True)
            else:
                st.success("Excellent! You have all the skills mentioned in the job description.")
                
        with tab_additional:
            if analysis["additional_skills"]:
                st.markdown("<p style='color: #718096; font-size: 0.9rem;'>These extra skills are in your resume but not explicitly requested by this JD:</p>", unsafe_allow_html=True)
                for s in analysis["additional_skills"]:
                    st.markdown(f'<span class="tag-pill tag-pill-additional">💡 {s}</span>', unsafe_allow_html=True)
            else:
                st.info("No additional skills detected.")
                
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # 6. Actionable Tips & Recommendations
        st.subheader("💡 Actionable Recommendations")
        for tip in analysis["tips"]:
            if "CRITICAL:" in tip:
                st.error(tip)
            elif "IMPROVEMENT:" in tip:
                st.warning(tip)
            elif "OPTIMIZATION:" in tip:
                st.info(tip)
            else:
                st.success(tip)
                
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # 7. Highlighted Keywords Resume Display
        st.subheader("📝 Resume Keyword Highlighting Viewer")
        st.markdown("<p style='color: #718096; font-size: 0.9rem;'>Below is your resume text with identified core skills & keywords highlighted:</p>", unsafe_allow_html=True)
        
        # Gather all terms to highlight (both matching skills and action verbs)
        highlight_terms = list(set(analysis["matching_skills"] + analysis["action_verbs_used"]))
        highlighted_html = highlight_keywords_in_html(res_text, highlight_terms)
        
        st.markdown(f"""
        <div style="background-color: #F7FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.5rem; max-height: 400px; overflow-y: scroll; font-family: monospace; white-space: pre-wrap; font-size: 0.9rem; color: #2D3748; line-height: 1.5;">
            {highlighted_html}
        </div>
        """, unsafe_allow_html=True)
        
        # 8. Download PDF Report Button (Sidebar action / bottom action)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with st.spinner("Generating PDF report..."):
            pdf_data = generate_pdf_report(analysis)
            
        st.download_button(
            label="📥 Download Detailed Analysis Report (PDF)",
            data=pdf_data,
            file_name=f"ATS_Score_Report_{strength}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        # Initial Placeholder UI before clicking analyze
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem; border: 2px dashed #CBD5E0; border-radius: 16px;">
            <span style="font-size: 3rem;">📊</span>
            <h3 style="margin-top: 1rem; color: #4A5568;">Ready for Analysis</h3>
            <p style="color: #718096; max-width: 400px; margin: 0.5rem auto 1.5rem auto;">
                Provide a resume PDF and a target job description on the left, then click <b>Analyze Resume Compatibility</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ----------------------------------------------------
# Sidebar Configurations
# ----------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.title("Settings & FAQ")
    
    st.markdown("""
    ### About the App
    This **AI Resume Analyzer & ATS Score Checker** parses the text from your resume PDF and compares it against the target Job Description using natural language processing (NLP).
    
    ### How It Works:
    1. **TF-IDF Vectorization** counts the frequency of words across both texts.
    2. **Cosine Similarity** evaluates the directional vector match, scoring the overall vocabulary alignment from 0 to 100.
    3. **Regex Boundary Scans** match complex tech skills (like C++, Node.js, SQL) against a structured skill library.
    4. **Recommendation Engine** outputs checklist feedback.
    
    *Built with Streamlit, Plotly, & ReportLab.*
    """)
    
    # Custom Dark Mode simulator toggle for styling test
    dark_mode_sim = st.toggle("Simulate Dark Theme")
    if dark_mode_sim:
        st.markdown("""
        <style>
            body {
                background-color: #121824;
                color: #EDF2F7;
            }
        </style>
        """, unsafe_allow_html=True)
