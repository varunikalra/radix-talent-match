import os
import json
import glob
import time
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from dotenv import load_dotenv
from google.genai.errors import ServerError

from llm import call_gemini
from prompts import RESUME_SYSTEM_PROMPT

load_dotenv()

RESUME_DIR = "sample_resumes"
OUTPUT_DIR = "resume_skills"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_single_resume(file_path: str):
    file_name = os.path.basename(file_path)
    ext = os.path.splitext(file_name)[1].lower()

    if ext == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        raw_text = extract_text_from_docx(file_path)
    else:
        print(f"Skipping unsupported file format: {file_name}")
        return

    print(f"Analyzing resume: {file_name}...")
    
    prompt = f"""
{RESUME_SYSTEM_PROMPT}

RESUME FILE NAME: {file_name}

RESUME TEXT CONTENT:
---
{raw_text}
---
"""

    response_text = None
    for attempt in range(3):
        try:
            response_text = call_gemini(prompt)
            break
        except ServerError:
            print(f"⚠️ Model busy (503). Retrying attempt {attempt + 1} in 5 seconds...")
            time.sleep(5)
    
    if not response_text:
        print(f"❌ Error: Failed to get response from Gemini for {file_name} due to high demand.")
        return

    # Clean up markdown code blocks if Gemini returns them
    cleaned_text = response_text.replace("```json", "").replace("```", "").strip()

    try:
        parsed_data = json.loads(cleaned_text)
        
        # Save output json
        output_filename = f"{Path(file_name).stem}_skills.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, indent=4)
            
        print(f"Successfully saved parsed skills to {output_path}")

    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON response for {file_name}")
        print("Raw response was:", response_text)

def run_batch_parser():
    supported_files = glob.glob(os.path.join(RESUME_DIR, "*.pdf")) + glob.glob(os.path.join(RESUME_DIR, "*.docx"))
    
    if not supported_files:
        print(f"No PDF or DOCX resumes found in '{RESUME_DIR}/'. Please add some sample resumes!")
        return

    for file_path in supported_files:
        file_name = os.path.basename(file_path)
        output_filename = f"{Path(file_name).stem}_skills.json"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        # Skip if already parsed
        if os.path.exists(output_path):
            print(f"Skipping {file_name} (already parsed)...")
            continue
            
        parse_single_resume(file_path)

if __name__ == "__main__":
    run_batch_parser()