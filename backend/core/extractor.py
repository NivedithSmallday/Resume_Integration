import json
import re
import docx2txt
import pdfplumber
from langchain_groq import ChatGroq
from .parser_prompt import resume_prompt


def clean_json_output(result: str) -> str:
    """
    Cleans LLM output by removing markdown code fences and trimming whitespace.
    """
    cleaned = re.sub(r"```(?:json)?", "", result, flags=re.IGNORECASE)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()


def extract_text_from_file(filepath: str) -> str:
    """
    Extract raw text from a PDF or DOCX file.
    """
    try:
        if filepath.endswith(".pdf"):
            with pdfplumber.open(filepath) as pdf:
                text = "\n".join(
                    page.extract_text() for page in pdf.pages if page.extract_text()
                )
                return text.strip()
        elif filepath.endswith(".docx"):
            return docx2txt.process(filepath).strip()
        else:
            print(f"⚠️ Unsupported file format: {filepath}")
            return ""
    except Exception as e:
        print(f"⚠️ Failed to extract text from {filepath}: {e}")
        return ""


class ResumeExtractor:
    """
    Uses Groq LLM to extract structured data from resumes.
    """

    def __init__(self, model_name: str = "qwen/qwen3-32b"):
        try:
            self.llm = ChatGroq(
                model=model_name,
                temperature=0,
                max_tokens=None,
                reasoning_format="parsed",
                timeout=None,
                max_retries=2,
            )
            # Create chain
            self.chain = resume_prompt | self.llm
        except Exception as e:
            raise RuntimeError(f"❌ Failed to initialize LLM: {e}")

    def extract(self, resume_text: str) -> dict:
        """
        Extract structured resume data using Groq LLM.
        """
        if not resume_text.strip():
            raise ValueError("⚠️ Empty resume text provided to extractor.")

        try:
            response = self.chain.invoke({"resume_text": resume_text})
            raw_output = getattr(response, "content", str(response))
            cleaned = clean_json_output(raw_output)

            try:
                parsed = json.loads(cleaned)
            except json.JSONDecodeError:
                raise ValueError(f"❌ LLM did not return valid JSON:\n{raw_output}")

            # Keep only DB schema keys
            allowed_keys = [
                "name",
                "email",
                "phone",
                "linkedin",
                "education",
                "experience",
                "career_span",
                "skills",
                "awards_or_achievements",
            ]

            result = {k: parsed.get(k, "") for k in allowed_keys}
            return result

        except Exception as e:
            print(f"❌ Error during LLM extraction: {e}")
            return {}
