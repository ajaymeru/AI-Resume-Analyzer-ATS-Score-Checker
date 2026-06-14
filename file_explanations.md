# AI Resume Analyzer & ATS Checker: Project Architecture & Files Guide

This guide explains the purpose, inputs, outputs, and design logic of each file in this project repository.

---

## 📁 Repository Overview & Directory Structure

```text
AI Resume Analyzer & ATS Score Checker/
│
├── app.py                  # Streamlit frontend dashboard & interactive GUI
├── analyzer.py             # NLP similarity metrics & resume evaluation engine
├── pdf_parser.py           # Clean plain text extractor for uploaded PDF files
├── report_generator.py     # PDF export generation layout compiler using ReportLab
│
├── requirements.txt        # Python dependency specification list
├── README.md               # Quick-start setup instructions & feature summary
└── file_explanations.md    # [This File] Documentation of the code design and architecture
```

---

## 📄 File Purposes & Explanations

### 1. `app.py`
* **Purpose**: Serves as the interactive graphical user interface (GUI) built with Streamlit.
* **Key Sections**:
  * **Theming / Styling**: Injects custom HTML/CSS for an elegant, responsive glassmorphism UI with customized google fonts (Outfit) and distinct pill tags for matching/missing skills.
  * **Predefined Sample JDs**: Holds built-in Job Descriptions (Full-Stack, Data Science, Product Manager) allowing immediate trial without pasting a description.
  * **HTML Highlighter Helper**: Highlights matched keywords (skills and action verbs) dynamically within the resume viewer, using regex substitutions.
  * **Layout Columns**: Uses a two-column setup:
    * *Left Column*: Receives user inputs (pasted JDs and file uploads).
    * *Right Column*: Renders dynamic gauges, pie charts, and keyword frequency graphs via Plotly, contact details scans, detailed skill maps, actionable suggestions, highlighted text, and the downloadable PDF report.

### 2. `analyzer.py`
* **Purpose**: The core analytical brain of the application. It processes the text parsing results and computes all logical checks and statistics.
* **Key Logical Functions**:
  * `detect_skills()`: Extracts skills from a predefined database matching special-character formats (e.g. `C++`, `Node.js`, `C#`) using precise negative lookbehind and lookahead regex boundaries (ensuring `git` doesn't match `digital`).
  * `calculate_ats_score()`: Applies TF-IDF vectorization and cosine similarity calculations between the resume and job description, applying a soft boost scaling factor of 1.35 to map mathematical similarity to standard, recruiter-friendly ATS score formats.
  * `check_contact_info()`: Runs regular expressions to scan for presence of GitHub links, LinkedIn profiles, phone numbers, and email addresses.
  * `extract_missing_keywords()`: Analyzes and sorts keyword frequencies in the Job Description, filtering out stopwords, to find critical terms missing in the resume.
  * `detect_action_verbs()`: Scans the resume for high-impact action verbs (e.g., *designed*, *automated*, *spearheaded*).
  * `analyze_resume()`: Aggregates all stats, checks word counts and reading metrics, maps categories (matching, missing, extra skills), and compiles a list of warnings/suggestions.

### 3. `pdf_parser.py`
* **Purpose**: Handles PDF document loading and extracts clean text to be processed by the engine.
* **Key Functions**:
  * `extract_text_from_pdf()`: Determines if the input is a file path string or a binary buffer (Streamlit's memory-based `BytesIO`). It opens the PDF using `PyPDF2.PdfReader`, iterates through all pages to extract text, and runs post-processing to trim extra whitespace and skip empty lines.

### 4. `report_generator.py`
* **Purpose**: Generates and compiles standard, professional PDF documents containing evaluation summaries.
* **Key Functions**:
  * `generate_pdf_report()`: Utilizes the `ReportLab` library to layout the analysis output. It defines document layout, styles (Helvetica font headings, body text, bullets, grids), formats metrics in a clean Executive Summary table, displays matching/missing skills mapping, highlights keywords to add, and lists action items as bullet points.

### 5. `requirements.txt`
* **Purpose**: Lists direct dependencies required to run the project.
* **Included Libraries**:
  * `streamlit`: The dashboard web application framework.
  * `pandas`: Data structuring library.
  * `pypdf2`: Lightweight PDF reader.
  * `scikit-learn`: NLP vectorizer and cosine similarity metrics.
  * `plotly`: Dynamic interactive charts (gauges, donuts, bar charts).
  * `reportlab`: Programmatic PDF report builder.

---

## 🔒 Ignored Files (in `.gitignore`)
To prevent configuration logs, cache directories, environment assets, or temporary documents from cluttering the GitHub source trees:
- `__pycache__/` and `*.pyc`
- `.venv/` and `env/` virtual environments
- `.env` local environment variable files
- `*.pdf` generated analysis reports and test resumes
- `file_explanations.md` (Specifically ignored to keep explanations local and out of Github repositories)
