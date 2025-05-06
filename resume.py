import docx2txt
import PyPDF2
import spacy
from nltk.tokenize import word_tokenize
nlp = spacy.load("en_core_web_sm")
REQUIRED_SKILLS = {"python", "machine learning", "data analysis", "nlp", "sql"}
REQUIRED_EDUCATION = {"bachelor", "master", "phd"}
def extract_text_from_pdf(pdf_path):
    text = "" 
    with open(pdf_path, "rb") as file:  
        reader = PyPDF2.PdfReader(file)  
        for page in reader.pages:  # Loop through each page in the PDF
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
    return {  # Return a dictionary with the results
        "matched_skills": list(matched_skills),  
        "matched_education": list(matched_education),  
        "score": score  # Return the total score
    }
def process_resume(file_path):
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)  
    else:
        return "Unsupported file format" 
    return screen_resume(text)
if __name__ == "__main__":
    resume_path = "ATS classic HR resume.docx"
    result = process_resume(resume_path)
    print(result)
