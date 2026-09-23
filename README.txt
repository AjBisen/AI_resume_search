AI RESUME ASSESSMENT PROJECT
==============================

Project Type:
Python + Flask + Resume Screening / Assessment

FEATURES
--------
1. Upload PDF, DOCX or TXT resume
2. Extract resume text
3. Enter job description / required skills
4. Detect common technical skills
5. Calculate a skill-match percentage
6. Show matched and missing skills
7. Show assessment status

PROJECT STRUCTURE
-----------------
AI_Resume_Assessment/
|
|-- app.py
|-- requirements.txt
|-- README.txt
|-- templates/
|   `-- index.html
`-- uploads/

HOW TO RUN ON WINDOWS
---------------------

1. Install Python 3.

2. Open CMD/PowerShell inside the project folder.

3. Create virtual environment:
   python -m venv venv

4. Activate it:
   venv\Scripts\activate

5. Install packages:
   python -m pip install -r requirements.txt

6. Start the application:
   python app.py

7. Open this address in browser:
   http://127.0.0.1:5000

DEMO
----
Upload a resume and enter:

Python, SQL, Pandas, Machine Learning, Power BI

The application will calculate a match score based on the detected skills.

NOTE
----
This is a practical educational resume-screening assessment project.
The score is a rule-based skill matching score, not a hiring decision.
