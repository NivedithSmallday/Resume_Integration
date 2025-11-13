from langchain.prompts import PromptTemplate

resume_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template="""
        You are a resume parser.

        Extract structured information from the resume below and return **only valid JSON**.
        Do not include explanations, markdown, or any text outside the JSON.

        Resume:
        {resume_text}

        Return JSON with the following keys only:
        - name (string)
        - email (string)
        - phone (string)
        - linkedin (string)
        - education (list of objects, each with: degree, field_of_study, institution, location, start_date, end_date, cgpa (float, if available), percentage (float, if available))
        - experience (list of objects: company, designation, start_date, end_date, responsibilities)
        - career_span (integer)
            - If explicitly mentioned in the resume (e.g., "10+ years of experience"), use that number.
            - Otherwise, calculate total years of professional experience from earliest start_date to latest end_date (or Present), rounded to nearest integer.
        - skills (list of strings)
        - awards_or_achievements (list of strings)

        Important:
        - Separate CGPA and percentage into distinct numeric fields if they exist.
        - Ensure JSON follows normalization (no nested free text blobs).
        - Output valid JSON only.
        """
)
