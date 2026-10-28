
# RADIX Talent Match - Role 1: JD Analytics

Automated LLM-powered data pipeline that ingests unstructured Job Descriptions (PDF/DOCX) and extracts standardized, structured skill profiles mapped to the 12 official RADIX categories.

## 📂 Project Structure

- `sample_jds/`: Contains raw input job description files (PDF/DOCX).
- `jd_skills/`: Output folder containing structured JSON files for each job description.
- `jd_analytics.py`: Main script for parsing documents and extracting categorized skills via Gemini.
- `validate_output.py`: Schema and category validation script.
- `api.py`: FastAPI backend server to serve the analyzed job data.

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
