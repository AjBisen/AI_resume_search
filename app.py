from flask import Flask, render_template, request
from docx import Document
import os
import re

# C:\Users\hp\AppData\Local\Programs\Python\Python314\python.exe app.py
#  run karne ke liye cmd 

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simple assessment skill bank
SKILLS = {
    "Python": ["python", "pandas", "numpy", "flask", "django"],
    "SQL": ["sql", "mysql", "postgresql", "postgres"],
    "Machine Learning": ["machine learning", "scikit-learn", "sklearn", "ml"],
    "Data Science": ["data science", "data analysis", "data analytics"],
    "Power BI": ["power bi", "powerbi", "dax"],
    "Excel": ["excel", "vlookup", "xlookup", "pivot table"],
    "Java": ["java", "spring", "spring boot"],
    "C/C++": ["c++", "c programming", "c language"],
    "Web Development": ["html", "css", "javascript", "react", "node.js"]
}

def extract_text_from_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            return ""

    if ext == ".docx":
        try:
            from docx import Document
            doc = Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            return ""

    return ""

def assess_resume(text, job_description):
    combined = (text + " " + job_description).lower()
    resume_lower = text.lower()

    found = []
    missing = []

    for skill, keywords in SKILLS.items():
        if any(re.search(r"\b" + re.escape(k.lower()) + r"\b", resume_lower) for k in keywords):
            found.append(skill)
        else:
            missing.append(skill)

    jd_keywords = []
    for skill, keywords in SKILLS.items():
        if any(k.lower() in job_description.lower() for k in keywords):
            jd_keywords.append(skill)

    if jd_keywords:
        matched_jd = [s for s in jd_keywords if s in found]
        score = round(len(matched_jd) / len(jd_keywords) * 100)
    else:
        score = round(min(100, len(found) / len(SKILLS) * 100))

    if score >= 70:
        status = "Strong Match"
    elif score >= 40:
        status = "Moderate Match"
    else:
        status = "Needs Improvement"

    return found, missing, score, status

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        resume = request.files.get("resume")
        job_description = request.form.get("job_description", "").strip()

        if not resume or resume.filename == "":
            return render_template("index.html", error="Please upload a resume.")

        safe_name = os.path.basename(resume.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)
        resume.save(path)

        text = extract_text_from_file(path)
        if not text.strip():
            return render_template(
                "index.html",
                error="Could not read the file. Use PDF, DOCX, or TXT."
            )

        found, missing, score, status = assess_resume(text, job_description)

        result = {
            "filename": safe_name,
            "score": score,
            "status": status,
            "found": found,
            "missing": missing
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
