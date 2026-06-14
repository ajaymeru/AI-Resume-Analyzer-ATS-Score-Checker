## Project: AI Resume Analyzer (100% Free, No API Keys)

This version is designed to be **resume-worthy**, realistic for a fresher, and can be generated almost entirely by Cursor/Antigravity from a single prompt.

# BRD (Business Requirements Document)

## Project Name

**AI Resume Analyzer & ATS Score Checker**

## Objective

Develop a web application that helps job seekers analyze their resumes against a job description and receive an ATS (Applicant Tracking System) compatibility score, missing skills analysis, and improvement suggestions.

## Problem Statement

Many candidates submit resumes that are not optimized for ATS systems. Recruiters often filter resumes based on keyword relevance and skill matching. Candidates need a simple tool to evaluate how well their resume matches a target job description.

## Target Users

* Students
* Fresh Graduates
* Job Seekers
* Career Switchers

## Functional Requirements

### Resume Upload

* Upload PDF resume
* Extract text from PDF
* Display extracted content

### Job Description Input

* Paste job description
* Validate input

### ATS Score Calculation

* Compare resume with job description
* Generate score from 0-100
* Display matching percentage

### Skill Analysis

* Identify matching skills
* Identify missing skills
* Highlight important keywords

### Resume Insights

* Total words
* Estimated reading time
* Contact information detection
* Skills count

### Recommendations

* Suggest missing keywords
* Suggest resume improvements
* Recommend stronger action verbs

### Dashboard

* ATS Score Card
* Skills Match Chart
* Missing Skills List
* Resume Statistics

### Export

* Download analysis report as PDF

---

## Non-Functional Requirements

### Performance

* Analysis under 5 seconds

### Security

* No data stored permanently
* Process files locally

### Usability

* Responsive UI
* Simple workflow

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### Libraries

* Streamlit
* Pandas
* PyPDF2
* Scikit-learn
* Plotly
* ReportLab
* Regex

---

## Project Structure

```text
resume-analyzer/
│
├── app.py
├── analyzer.py
├── pdf_parser.py
├── report_generator.py
├── requirements.txt
├── README.md
│
├── assets/
│
└── sample_data/
```

---

# Master Prompt for Cursor / Antigravity

Copy everything below:

```text id="4m0yy0"
Build a production-quality Python project called "AI Resume Analyzer & ATS Score Checker".

Requirements:

TECH STACK:
- Python
- Streamlit
- Pandas
- PyPDF2
- Scikit-learn
- Plotly
- ReportLab

FEATURES:

1. Resume Upload
- Upload PDF resume
- Extract text using PyPDF2
- Display extracted text

2. Job Description Input
- Multi-line text area
- User can paste any job description

3. ATS Score Engine
- Compare resume and job description using TF-IDF Vectorization
- Use Cosine Similarity
- Generate ATS Score from 0-100

4. Skill Detection
Create predefined skill database including:
Python
Java
JavaScript
React
Node.js
SQL
MongoDB
AWS
Docker
Kubernetes
Git
Machine Learning
Data Analysis
Power BI
Excel

Detect:
- Skills found in resume
- Skills found in job description
- Missing skills

5. Resume Statistics
Display:
- Word Count
- Character Count
- Number of Skills Found
- ATS Score
- Resume Strength Level

Strength Levels:
0-40 = Weak
41-70 = Average
71-85 = Good
86-100 = Excellent

6. Recommendations Engine
Generate suggestions:
- Missing skills
- Missing keywords
- Action verbs suggestions
- Resume optimization tips

7. Dashboard UI
Professional modern UI using Streamlit.

Sections:
- Header
- Upload Resume
- Paste Job Description
- ATS Score Card
- Skill Analysis
- Resume Statistics
- Recommendations

8. Visualizations
Use Plotly charts:
- ATS Score Gauge
- Skill Match Pie Chart
- Missing Skills Bar Chart

9. PDF Report
Generate downloadable PDF report containing:
- ATS Score
- Skills Found
- Missing Skills
- Recommendations

10. Code Quality
- Modular architecture
- Separate files for parsing, analysis, reporting
- Type hints
- Error handling
- Comments
- Clean code

11. README
Generate professional README with:
- Features
- Installation
- Screenshots section
- Tech Stack
- Usage

12. requirements.txt
Generate all dependencies.

13. UI Styling
Use custom CSS.
Create recruiter-friendly professional appearance.

14. Bonus Features
- Dark mode toggle
- Resume keyword highlighting
- Progress indicators
- Download report button

OUTPUT:
Generate complete project files with folder structure and fully working code.
```

---

### Resume Entry After Completion

**Project: AI Resume Analyzer & ATS Score Checker**

* Developed a resume analysis platform using Python, Streamlit, and NLP techniques to evaluate ATS compatibility and job-description matching.
* Implemented TF-IDF vectorization and cosine similarity algorithms to generate resume-job match scores and identify skill gaps.
* Built interactive dashboards and PDF reporting features for resume optimization insights and recruiter-focused recommendations.

This looks significantly stronger on a fresher resume than a basic CRUD app while remaining achievable without any paid APIs.
