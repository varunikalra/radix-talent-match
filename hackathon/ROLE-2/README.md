
# RADIX Role 2: Resume Parser & Skill Matching

Role 2 is a FastAPI-based backend service designed to ingest candidate resumes (PDF or DOCX), extract their technical skills using Gemini, and standardize them into the official **12 RADIX categories** (`COD`, `DSA`, `OOD`, `COMM`, `AI`, `APTI`, `CLOUD`, `SYSD`, `SQL`, `SWE`, `NETW`, `OS`, or `OTHER`).

---

## Project Directory Structure

```text
ROLE-2/
├── sample_resumes/      # Place candidate PDF/DOCX resumes here
├── resume_skills/       # Output folder for parsed JSON skill profiles
├── profile_prefill/     # Output folder for Profile Builder data
├── llm.py               # Google Gemini client wrapper
├── prompts.py           # System prompts and extraction logic
├── resume_parser.py     # Core script for batch/single resume parsing
├── validate_output.py   # Script to validate JSON against RADIX schema
├── api.py               # FastAPI backend server endpoints
├── requirements.txt     # Python dependencies
├── .env                 # Private environment variables (API keys)
└── .gitignore           # Git ignore rules
```
