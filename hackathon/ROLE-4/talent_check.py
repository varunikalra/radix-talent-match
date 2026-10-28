import os
import json
from pathlib import Path

PROFILE_DIR = "../ROLE-3/candidate_profiles"
CHECKS_DIR = "checks"
os.makedirs(CHECKS_DIR, exist_ok=True)

def run_talent_check(candidate_name: str) -> dict:
    """
    Evaluates a candidate profile against standard RADIX eligibility and criteria checks.
    """
    filename = f"{candidate_name.lower().replace(' ', '_')}_profile.json"
    file_path = os.path.join(PROFILE_DIR, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Candidate profile for {candidate_name} not found at {file_path}")
        
    with open(file_path, "r", encoding="utf-8") as f:
        profile = json.load(f)
        
    # Example evaluation logic for Talent Check (Role 4)
    has_degree = len(profile.get("education", [])) > 0
    has_skills = len(profile.get("skills", [])) > 0
    
    status = "APPROVED" if (has_degree and has_skills) else "REVIEW_REQUIRED"
    
    report = {
        "candidate_name": profile.get("name"),
        "email": profile.get("email"),
        "eligibility_status": status,
        "checks_performed": {
            "education_verified": has_degree,
            "skills_present": has_skills
        }
    }
    
    # Save check report
    report_filename = f"{candidate_name.lower().replace(' ', '_')}_check_report.json"
    report_path = os.path.join(CHECKS_DIR, report_filename)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
        
    print(f"✅ Talent check complete for {candidate_name}. Status: {status}")
    return report

if __name__ == "__main__":
    # Test check on Ananya Rao
    run_talent_check("Ananya Rao")