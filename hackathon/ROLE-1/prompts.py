from langchain_core.prompts import PromptTemplate

JD_EXTRACTION_PROMPT = PromptTemplate(
    input_variables=["jd_text"],
    template="""
You are an expert technical recruiter and data extractor for RADIX. 
Your task is to analyze the provided Job Description (JD) text and extract a structured list of required skills and technologies.

The skill signal is heavily concentrated in sections like "Key Responsibilities" and "What We're Looking For". Focus your search there[cite: 7].

Every extracted skill MUST be assigned to EXACTLY ONE of the following 12 official RADIX category codes (if it does not fit any, use "OTHER")[cite: 9]:
- COD (Coding)[cite: 9]
- DSA (Data Structures & Algorithms)[cite: 9]
- OOD (Object-Oriented Design)[cite: 9]
- COMM (Communication)[cite: 9]
- AI (AI)[cite: 9]
- APTI (Aptitude)[cite: 9]
- CLOUD (Cloud)[cite: 9]
- SYSD (System Design)[cite: 9]
- SQL (SQL)[cite: 9]
- SWE (Software Engineering)[cite: 9]
- NETW (Networking)[cite: 9]
- OS (Operating Systems)[cite: 9]

Return the response in valid JSON format matching this exact schema:
{{
    "source_type": "jd",
    "source_file": "filename_placeholder",
    "company": "Company Name",
    "role": "Role Title",
    "skills": [
        {{
            "skill_name": "Name of skill or technology",
            "category_code": "ONE OF THE 12 CODES OR OTHER",
            "evidence": "Short quote or reason from text",
            "confidence": "high|medium|low"
        }}
    ]
}}

Here is the Job Description text to analyze:
{jd_text}
"""
)