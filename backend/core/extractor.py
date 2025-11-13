import json
import re
from langchain_groq import ChatGroq
from .parser_prompt import resume_prompt
import re
import docx2txt
import pdfplumber


def clean_json_output(result: str) -> str:
    """
    Cleans LLM output by removing markdown code fences and trimming whitespace.
    """
    # remove ```json ... ``` or ``` ... ```
    cleaned = re.sub(r"```(?:json)?", "", result, flags=re.IGNORECASE)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()

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


class ResumeExtractor:
    """Uses Groq LLM to extract structured data from resumes."""

    def __init__(self, model_name="qwen/qwen3-32b"):
        self.llm = ChatGroq(
            model=model_name,
            temperature=0,
            max_tokens=None,
            reasoning_format="parsed",  # ensures structured output
            timeout=None,
            max_retries=2,
        )
        # Modern chaining syntax: prompt | llm
        self.chain = resume_prompt | self.llm

    def extract(self, resume_text: str) -> dict:
        # print(resume_text)
        """Extract structured resume data using Groq LLM."""
        # Invoke chain (returns AIMessage)
        response = self.chain.invoke({"resume_text": resume_text})

        # Get text content from AIMessage
        raw_output = getattr(response, "content", str(response))

        # Clean extra fences
        cleaned = clean_json_output(raw_output)
        print(cleaned)

        try:
            parsed = json.loads(cleaned)

            # keep only DB schema keys
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
            return {k: parsed.get(k) for k in allowed_keys}
        except json.JSONDecodeError:
            raise ValueError(f"LLM did not return valid JSON:\n{raw_output}")
