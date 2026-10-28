import os
import glob
import json
import time
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document
from google import genai

load_dotenv()

client = genai.Client()

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def process_job_descriptions():
    os.makedirs("jd_skills", exist_ok=True)
    
    pdf_files = glob.glob("sample_jds/*.pdf")
    docx_files = glob.glob("sample_jds/*.docx")
    all_files = pdf_files + docx_files
    
    if not all_files:
        print("No job descriptions found in 'sample_jds/' folder!")
        return

    print(f"Found {len(all_files)} job description(s) to process.\n")

    for file_path in all_files:
        filename = os.path.basename(file_path)
        print(f"Processing: {filename}...")
        
        if file_path.endswith(".pdf"):
            jd_text = extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            jd_text = extract_text_from_docx(file_path)
        else:
            continue
        
        prompt = f"""
You are an expert technical recruiter and data extractor for RADIX. 
Analyze the provided Job Description text and extract a structured list of required skills and technologies.
Focus heavily on sections like "Key Responsibilities" and "What We're Looking For".

Every extracted skill MUST be assigned to EXACTLY ONE of these 12 official RADIX category codes (otherwise use "OTHER"):
- COD, DSA, OOD, COMM, AI, APTI, CLOUD, SYSD, SQL, SWE, NETW, OS

Return ONLY valid JSON matching this exact structure (no extra markdown text):
{{
    "source_type": "jd",
    "source_file": "{filename}",
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

        # Try up to 3 times if the server is busy
        success = False
        for attempt in range(3):
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
                raw_content = raw_content.strip()
                
                parsed_json = json.loads(raw_content)
                parsed_json["source_file"] = filename
                
                output_filename = filename.rsplit(".", 1)[0] + ".json"
                output_path = os.path.join("jd_skills", output_filename)
                
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(parsed_json, f, indent=4)
                    
                print(f"Successfully extracted and saved: {output_filename}\n")
                success = True
                break
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {filename}: {e}")
                if attempt < 2:
                    print("Retrying in 3 seconds...")
                    time.sleep(3)
                else:
                    print(f"Error processing {filename} after 3 attempts.\n")

if __name__ == "__main__":
    process_job_descriptions()