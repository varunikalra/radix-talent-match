import os
import json

PROFILE_DIR = "../ROLE-3/candidate_profiles"
CHECKS_DIR = "checks"
os.makedirs(CHECKS_DIR, exist_ok=True)

candidates = [
    "Ananya Rao",
    "Karthik Subramaniam",
    "Priya Menon",
    "Rohan Verma"
]

def run_all():
    print(f"🔍 Running talent checks for {len(candidates)} candidates...\n")
    for name in candidates:
        filename = f"{name.lower().replace(' ', '_')}_profile.json"
        file_path = os.path.join(PROFILE_DIR, filename)
        
        if not os.path.exists(file_path):
            print(f"❌ Profile not found for {name}")
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            profile = json.load(f)
            
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
        
        report_filename = f"{name.lower().replace(' ', '_')}_check_report.json"
        report_path = os.path.join(CHECKS_DIR, report_filename)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
            
        print(f"✅ Generated check report for {name} -> Status: {status}")

if __name__ == "__main__":
    run_all()