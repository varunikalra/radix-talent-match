from fastapi import FastAPI, HTTPException
import os
import json
from skill_matcher import compute_skill_match

app = FastAPI(title="RADIX Skill Matcher API", version="1.0")

MATCHES_DIR = "matches"
os.makedirs(MATCHES_DIR, exist_ok=True)

@app.post("/match/{candidate_name}")
def match_candidate_endpoint(candidate_name: str):
    try:
        report = compute_skill_match(candidate_name)
        return {"status": "success", "report": report}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/match/{candidate_name}")
def get_match_endpoint(candidate_name: str):
    report_filename = f"{candidate_name.lower().replace(' ', '_')}_match_report.json"
    report_path = os.path.join(MATCHES_DIR, report_filename)
    
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Match report not found")
        
    with open(report_path, "r", encoding="utf-8") as f:
        return json.load(f)