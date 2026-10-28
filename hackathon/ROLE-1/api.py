from fastapi import FastAPI, HTTPException, UploadFile, File
import os
import json
from pypdf import PdfReader
from docx import Document
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

app = FastAPI(title="RADIX JD Analytics API", version="1.0")

VALID_CATEGORIES = {"COD", "DSA", "OOD", "COMM", "AI", "APTI", "CLOUD", "SYSD", "SQL", "SWE", "NETW", "OS", "OTHER"}

@app.get("/")
def home():
    return {"message": "Welcome to the RADIX JD Analytics API!"}

@app.get("/jds")
def get_all_jds():
    """Returns a list of all processed job descriptions stored in jd_skills/."""
    if not os.path.exists("jd_skills"):
        return []
    
    results = []
    for file in os.listdir("jd_skills"):
        if file.endswith(".json"):
            with open(os.path.join("jd_skills", file), "r", encoding="utf-8") as f:
                results.append(json.load(f))
    return results

@app.get("/jds/{filename}")
def get_jd_by_filename(filename: str):
    """Fetch a specific parsed job description by its JSON filename."""
    path = os.path.join("jd_skills", filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Job description analysis not found")
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/analyse-jd")
async def analyse_jd_endpoint(file: UploadFile = File(...)):
    """Upload a new PDF or DOCX Job Description file to parse and extract structured skills dynamically."""
    os.makedirs("temp_uploads", exist_ok=True)
    file_path = os.path.join("temp_uploads", file.filename)
    
    # Save uploaded file temporarily
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
        
    # Extract text based on extension
    jd_text = ""
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            jd_text += page.extract_text() or ""
    elif file.filename.endswith(".docx"):
        doc = Document(file_path)
        jd_text = "\n".join([p.text for p in doc.paragraphs])
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
        
    prompt = f"""
You are an expert technical recruiter and data extractor for RADIX. 
Analyze the provided Job Description text and extract a structured list of required skills and technologies.
Focus heavily on sections like "Key Responsibilities" and "What We're Looking For".

Every extracted skill MUST be assigned to EXACTLY ONE of these 12 official RADIX category codes (otherwise use "OTHER"):
- COD, DSA, OOD, COMM, AI, APTI, CLOUD, SYSD, SQL, SWE, NETW, OS

Return ONLY valid JSON matching this exact structure (no extra markdown text):
{{
    "source_type": "jd",
    "source_file": "{file.filename}",
    "company": "Company Name",
    "role": "Role Title",
    "skills": [
        {{
            "skill_name": "Name of skill or technology",
            "category_code": "ONE OF THE 12 CODES OR OTHER",
            "evidence": "Short quote or reason from text",
            "confidence": "high"
        }}
    ]
}}

Job Description Text:
{jd_text}
"""

    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
        )
        raw_content = response.text.strip()
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:]
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
        
        parsed_json = json.loads(raw_content.strip())
        return parsed_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM extraction failed: {str(e)}")