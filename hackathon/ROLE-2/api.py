import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from resume_parser import parse_single_resume

app = FastAPI(title="RADIX Role 2: Resume Parser API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "sample_resumes"
OUTPUT_DIR = "resume_skills"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/parse-resume/")
async def upload_and_parse_resume(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx", ".doc")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save uploaded file locally
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    try:
        # Run the parser logic
        parse_single_resume(file_path)
        
        # Load the resulting json to return in response
        output_filename = f"{Path(file.filename).stem}_skills.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        if os.path.exists(output_path):
            with open(output_path, "r", encoding="utf-8") as f:
                parsed_data = json.load(f)
            return {"status": "success", "data": parsed_data}
        else:
            raise HTTPException(status_code=500, detail="Parsing completed but output file was not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "Role 2 API is running successfully"}