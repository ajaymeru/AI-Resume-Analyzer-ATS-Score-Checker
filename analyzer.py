import re
from typing import List, Dict, Any, Set
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Predefined skill database
PREDEFINED_SKILLS: List[str] = [
    "Python", "Java", "JavaScript", "React", "Node.js", "SQL", "MongoDB", "AWS", 
    "Docker", "Kubernetes", "Git", "Machine Learning", "Data Analysis", "Power BI", "Excel",
    "C++", "C#", "HTML", "CSS", "TypeScript", "Angular", "Vue.js", "Django", "Flask",
    "PostgreSQL", "MySQL", "NoSQL", "DevOps", "CI/CD", "Cloud Computing", "Azure", "GCP",
    "PyTorch", "TensorFlow", "Pandas", "NumPy", "Scikit-learn", "Linux", "REST API", "GraphQL",
    "Spring Boot", "Rust", "Go", "Ruby", "PHP", "Swift", "Kotlin", "Tableau", "Jira", "Agile"
]

# Action verbs commonly suggested for resumes
ACTION_VERBS: List[str] = [
    "achieved", "acquired", "adapted", "addressed", "administered", "advised", "allocated",
    "analyzed", "anticipated", "applied", "approved", "arranged", "assembled", "assessed",
    "assigned", "assisted", "attained", "audited", "authored", "automated", "balanced",
    "budgeted", "built", "calculated", "cataloged", "categorized", "chaired", "clarified",
    "classified", "coached", "collaborated", "collected", "communicated", "compared",
    "compiled", "completed", "composed", "computed", "conceptualized", "conducted",
    "consolidated", "constructed", "consulted", "contracted", "contributed", "controlled",
    "coordinated", "counseled", "created", "critiqued", "cultivated", "customized",
    "debated", "decided", "defined", "delegated", "delivered", "demonstrated", "designed",
    "detected", "determined", "developed", "devised", "diagnosed", "directed", "discovered",
    "dispatched", "distinguished", "distributed", "documented", "drafted", "edited",
    "educated", "eliminated", "enabled", "enforced", "engineered", "established", "estimated",
    "evaluated", "examined", "executed", "expanded", "expedited", "explained", "facilitated",
    "financed", "forecasted", "formulated", "fostered", "founded", "gathered", "generated",
    "guided", "handled", "headed", "identified", "illustrated", "implemented", "improved",
    "improvised", "incorporated", "increased", "influenced", "informed", "initiated",
    "inspected", "inspired", "installed", "instructed", "integrated", "interpreted",
    "introduced", "invented", "investigated", "launched", "lectured", "led", "licensed",
    "maintained", "managed", "marketed", "measured", "mediated", "mentored", "merged",
    "minimized", "modeled", "moderated", "monitored", "motivated", "negotiated", "obtained",
    "operated", "optimized", "orchestrated", "organized", "originated", "overhauled",
    "oversaw", "participated", "performed", "persuaded", "photographed", "planned",
    "prepared", "presented", "presided", "printed", "prioritized", "processed", "produced",
    "programmed", "projected", "promoted", "proposed", "provided", "publicized", "published",
    "purchased", "recommended", "reconciled", "recorded", "recruited", "redesigned",
    "referred", "regulated", "rehabilitated", "remodeled", "reorganized", "repaired",
    "reported", "represented", "researched", "resolved", "responded", "restructured",
    "retrieved", "reviewed", "revised", "scheduled", "screened", "selected", "served",
    "shaped", "simulated", "solved", "spearheaded", "sponsored", "staffed", "standardized",
    "stimulated", "streamlined", "structured", "studied", "supervised", "supported",
    "surveyed", "synthesized", "systematized", "tabulated", "taught", "tested", "trained",
    "translated", "updated", "upgraded", "utilized", "validated", "verified", "wrote"
]

# Stopwords for keyword analysis
STOPWORDS: Set[str] = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", "experience", "role", "work",
    "team", "skills", "job", "description", "requirements", "candidate", "responsibilities", "using", "working"
}


def detect_skills(text: str, skills_list: List[str] = PREDEFINED_SKILLS) -> List[str]:
    """
    Detects skills from a predefined list within a given text, utilizing word boundary matching
    that accommodates special characters (e.g., C++, Node.js).
    """
    found_skills = []
    text_lower = text.lower()
    for skill in skills_list:
        skill_lower = skill.lower()
        # Escape any special characters for regex safety
        escaped_skill = re.escape(skill_lower)
        # Use boundary assertions that prevent matching within alphanumeric substrings
        # e.g., 'git' shouldn't match 'digital' or 'git-hub'
        pattern = r'(?<![a-zA-Z0-9_])' + escaped_skill + r'(?![a-zA-Z0-9_])'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    return found_skills


def calculate_ats_score(resume_text: str, jd_text: str) -> float:
    """
    Calculates the ATS match score using TF-IDF Vectorization and Cosine Similarity.
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
    
    # Create the vectorizer with built-in english stop words
    vectorizer = TfidfVectorizer(stop_words='english')
    
    try:
        # Generate the TF-IDF representation
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        # Compute cosine similarity between resume (idx 0) and jd (idx 1)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        score = float(similarity[0][0]) * 100
        # Let's normalize it slightly: Cosine similarity of text documents can naturally be low 
        # even for high quality matches due to formatting. We apply a soft scaling factor 
        # to make it align with realistic ATS expectations (e.g. mapping 0-1 similarity to standard 0-100 score).
        # We'll use a moderate logarithmic booster or cap at 100. Let's do a simple boost:
        # Boost formula: similarity * 1.5 capped at 1.0, or just keep it direct.
        # Let's keep it direct but offer a normalized score to ensure it is recruiter-friendly.
        # Let's do: normalized_score = min(100.0, score * 1.3) to represent a reasonable score.
        normalized_score = min(100.0, score * 1.35)
        return round(normalized_score, 1)
    except Exception:
        return 0.0


def check_contact_info(text: str) -> Dict[str, bool]:
    """
    Checks if common contact details (email, phone, LinkedIn, GitHub) are present in the resume text.
    """
    has_email = bool(re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text))
    has_phone = bool(re.search(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3,4}\)?[-.\s]?\d{3}[-.\s]?\d{4,6}', text))
    has_linkedin = bool(re.search(r'linkedin\.com/in/[a-zA-Z0-9_-]+', text, re.IGNORECASE))
    has_github = bool(re.search(r'github\.com/[a-zA-Z0-9_-]+', text, re.IGNORECASE))
    
    return {
        "email": has_email,
        "phone": has_phone,
        "linkedin": has_linkedin,
        "github": has_github
    }


def extract_missing_keywords(resume_text: str, jd_text: str) -> List[str]:
    """
    Extracts high-frequency keywords from the job description that are missing in the resume.
    """
    resume_words = set(re.findall(r'\b[a-z]{3,}\b', resume_text.lower()))
    jd_words = re.findall(r'\b[a-z]{3,}\b', jd_text.lower())
    
    # Filter stopwords
    filtered_jd_words = [w for w in jd_words if w not in STOPWORDS]
    
    # Frequency count
    word_counts = Counter(filtered_jd_words)
    
    # Get top 20 keywords from JD
    top_jd_keywords = [item[0] for item in word_counts.most_common(25)]
    
    # Identify which ones are not in the resume
    missing_keywords = [w for w in top_jd_keywords if w not in resume_words]
    return missing_keywords


def detect_action_verbs(text: str) -> List[str]:
    """
    Detects which standard action verbs are used in the resume.
    """
    found_verbs = []
    text_lower = text.lower()
    for verb in ACTION_VERBS:
        pattern = r'\b' + re.escape(verb) + r'\b'
        if re.search(pattern, text_lower):
            found_verbs.append(verb)
    return found_verbs


def analyze_resume(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Combines parsing, math vector similarity, and keyword processing to run full analysis.
    """
    # 1. Statistics
    word_count = len(resume_text.split())
    char_count = len(resume_text)
    reading_time = max(1, round(word_count / 200))
    
    # 2. Skill Detection
    resume_skills = detect_skills(resume_text)
    jd_skills = detect_skills(jd_text)
    
    matching_skills = sorted(list(set(resume_skills) & set(jd_skills)))
    missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))
    additional_skills = sorted(list(set(resume_skills) - set(jd_skills)))
    
    # 3. ATS Score
    ats_score = calculate_ats_score(resume_text, jd_text)
    
    # 4. Strength Level
    if ats_score <= 40:
        strength = "Weak"
    elif ats_score <= 70:
        strength = "Average"
    elif ats_score <= 85:
        strength = "Good"
    else:
        strength = "Excellent"
        
    # 5. Contact info check
    contact_info = check_contact_info(resume_text)
    
    # 6. Action Verbs
    verbs_used = detect_action_verbs(resume_text)
    
    # 7. Keywords Missing
    missing_keywords = extract_missing_keywords(resume_text, jd_text)
    
    # 8. Tips generation
    tips = []
    if not contact_info["email"]:
        tips.append("CRITICAL: Add your email address to the resume.")
    if not contact_info["phone"]:
        tips.append("CRITICAL: Add your phone number so recruiters can reach you.")
    if not contact_info["linkedin"]:
        tips.append("SUGGESTION: Include your LinkedIn profile link to showcase professional network.")
    if len(verbs_used) < 8:
        tips.append("IMPROVEMENT: Integrate more strong action verbs (e.g., 'spearheaded', 'orchestrated') to describe responsibilities.")
    if word_count < 200:
        tips.append("IMPROVEMENT: Your resume content is extremely short. Try to add more details about projects or work experience.")
    elif word_count > 1000:
        tips.append("IMPROVEMENT: Your resume is a bit verbose (over 1000 words). Try to condense it to 1-2 pages of high-impact points.")
    if len(missing_skills) > 0:
        tips.append(f"OPTIMIZATION: Incorporate some of the missing skills like {', '.join(missing_skills[:3])} to match the JD requirements.")
    if len(missing_keywords) > 0:
        tips.append(f"OPTIMIZATION: Add these relevant terms from the JD: {', '.join(missing_keywords[:4])}.")
        
    if not tips:
        tips.append("Great job! Your resume format and content density are strong. Make sure to keep updating achievements with quantitative results.")
        
    return {
        "word_count": word_count,
        "char_count": char_count,
        "reading_time": reading_time,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "ats_score": ats_score,
        "strength_level": strength,
        "contact_info": contact_info,
        "action_verbs_used": verbs_used,
        "missing_keywords": missing_keywords,
        "tips": tips
    }
