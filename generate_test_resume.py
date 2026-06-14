from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def main():
    doc = SimpleDocTemplate("test_resume.pdf")
    styles = getSampleStyleSheet()
    
    story = [
        Paragraph("Ajay Maurya", styles["Heading1"]),
        Paragraph("Email: ajay@example.com | Phone: +91 9876543210", styles["Normal"]),
        Paragraph("GitHub: github.com/ajay | LinkedIn: linkedin.com/in/ajay", styles["Normal"]),
        Spacer(1, 10),
        Paragraph("Skills: Python, JavaScript, React, Node.js, SQL, MongoDB, Git, Docker, AWS, Machine Learning, DevOps, HTML, CSS", styles["Normal"]),
        Spacer(1, 10),
        Paragraph("Experience & Projects:", styles["Heading2"]),
        Paragraph("- Full-Stack Web App: Built using React, Node.js, and MongoDB. Configured Docker containerization and deployed on AWS EC2 instances.", styles["Normal"]),
        Paragraph("- Resume ATS Checker: Developed a Streamlit web app in Python. Used Scikit-learn for similarity scoring and ReportLab for PDF generation.", styles["Normal"]),
        Paragraph("- Optimized database queries using PostgreSQL indexes and led a team of 3 developers to achieve a 20% performance boost.", styles["Normal"])
    ]
    
    doc.build(story)
    print("test_resume.pdf successfully created!")


if __name__ == "__main__":
    main()
