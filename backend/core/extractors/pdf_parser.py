import re
import docx2txt
import pdfplumber

def extract_text_from_file(filepath):
    try:
        if filepath.endswith('.pdf'):
            with pdfplumber.open(filepath) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        elif filepath.endswith('.docx'):
            return docx2txt.process(filepath)
        else:
            return ""
    except Exception as e:
        print(f"⚠️ Failed to extract text from {filepath}: {e}")
        return ""


import re

def parse_resume(text):
    # Try to extract name from common patterns
    name_match = re.search(r"(?:Name[:\-]?\s*)([A-Z][a-z]+\s+[A-Z][a-z]+)", text)

    # Try to extract experience in years
    exp_match = re.search(r"(\d+)\s+(?:years|yrs)\s+(?:of\s+)?(?:experience|exp)", text, re.IGNORECASE)

    # Extract skills from a predefined list
    skill_keywords = ['Python', 'Java', 'SQL', 'Excel', 'C++', 'Machine Learning', 'Data Analysis', 'AWS', 'JavaScript']
    skills_found = [
        skill for skill in skill_keywords
        if re.search(rf"\b{re.escape(skill)}\b", text, re.IGNORECASE)
    ]

    return {
        "name": name_match.group(1) if name_match else "Unknown",
        "experience": f"{exp_match.group(1)} years" if exp_match else "Not specified",
        "skills": list(set(skills_found))
    }

