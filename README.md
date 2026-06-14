# AI Resume Analyzer & ATS Score Checker

A professional, NLP-powered resume analysis web platform built with Python and Streamlit. It calculates Applicant Tracking System (ATS) compatibility, flags missing skills, maps keywords, and generates downloadable PDF evaluation reports.

---

## 🌟 Features

- **PDF Text Parsing**: Automatically extracts text from uploaded PDF resumes using `PyPDF2`.
- **ATS Similarity Engine**: Compares the resume against the job description using TF-IDF vectorization and Cosine Similarity, generating a score between 0 and 100.
- **Skill Detection & Gap Mapping**: Detects matching, missing, and extra skills from a database of common developer/managerial skills (handling complex terms like C++, Node.js, and C# seamlessly via custom boundary word regex).
- **Interactive Visualizations**: Displays Plotly-powered gauges, donut charts for skill ratios, and frequency graphs of missing keywords.
- **Actionable Feedback**: Generates automated improvement guidelines (e.g. action verbs, length optimization, email/phone checks).
- **Report Lab PDF Exports**: Compiles and exports standard professional PDF reports for download.
- **Keyword Highlighter**: Highlights matched keywords directly in the resume text viewer.
- **Dark Mode Simulation**: Toggle dark interface container theme instantly.
- **Predefined Sample Datasets**: Try out the app instantly using sample resumes and job descriptions without uploading a file.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit, Custom HTML/CSS
- **NLP / Engine**: Scikit-Learn (`TfidfVectorizer`, `cosine_similarity`), Regex
- **Graphics / Visuals**: Plotly (`go.Indicator`, `go.Pie`, `go.Bar`)
- **PDF Generation**: ReportLab (`SimpleDocTemplate`, `TableStyle`, Flowables)
- **PDF Parsing**: PyPDF2 (`PdfReader`)
- **Language**: Python 3.12+

---

## 📁 Project Structure

```text
AI Resume Analyzer & ATS Score Checker/
│
├── app.py                  # Main Streamlit user interface & dashboard
├── analyzer.py             # NLP scoring, skill matching, and logic algorithms
├── pdf_parser.py           # Helper utility to extract text from PDF files
├── report_generator.py     # PDF report compiler using ReportLab
│
├── requirements.txt        # Python dependency specifications
└── README.md               # User manual & project documentation
```

---

## 🚀 Installation & Setup

1. **Clone or Open this Project Directory**:
   ```bash
   cd "AI Resume Analyzer & ATS Score Checker"
   ```

2. **Set up a Virtual Environment** (Optional but Recommended):
   ```bash
   py -m venv venv
   # Activate on Windows:
   .\venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   py -m pip install -r requirements.txt
   ```

4. **Launch the Web Dashboard**:
   ```bash
   py -m streamlit run app.py
   ```

5. **Access the App**:
   Open [http://localhost:8501](http://localhost:8501) in your browser.
