from flask import Flask, render_template, request
import docx2txt
import PyPDF2
import spacy
from nltk.tokenize import word_tokenize
import os

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

REQUIRED_SKILLS = {"python", "machine learning", "data analysis", "nlp", "sql"}
REQUIRED_EDUCATION = {"bachelor", "master", "phd"}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text

def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

def screen_resume(resume_text):
    resume_text = resume_text.lower()
    tokens = set(word_tokenize(resume_text))

    matched_skills = REQUIRED_SKILLS.intersection(tokens)
    matched_education = REQUIRED_EDUCATION.intersection(tokens)

    score = len(matched_skills) + len(matched_education)

    return {
        "matched_skills": list(matched_skills),
        "matched_education": list(matched_education),
        "score": score
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        file = request.files["resume"]

        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            if file.filename.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif file.filename.endswith(".docx"):
                text = extract_text_from_docx(file_path)
            else:
                return "Unsupported file format"

            result = screen_resume(text)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)