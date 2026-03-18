from flask import Flask, render_template, request
import docx2txt
import PyPDF2
import spacy
from nltk.tokenize import word_tokenize
import nltk
import os

app = Flask(__name__)

# ✅ Fix NLTK
nltk.download('punkt')

# ❌ REMOVE runtime download
# spacy.cli.download("en_core_web_sm")

# ✅ Load safely
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None  # fallback (avoid crash)

REQUIRED_SKILLS = {"python", "machine learning", "data analysis", "nlp", "sql"}
REQUIRED_EDUCATION = {"bachelor", "master", "phd"}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:   # ✅ Fix None error
                text += page_text + " "
    return text

def extract_text_from_docx(docx_path):
    return docx2txt.process(docx_path)

def screen_resume(resume_text):
    resume_text = resume_text.lower()

    try:
        tokens = set(word_tokenize(resume_text))
    except:
        tokens = set(resume_text.split())  # fallback

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
        try:
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

        except Exception as e:
            return f"Error: {str(e)}"  # ✅ shows real error

    return render_template("index.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
