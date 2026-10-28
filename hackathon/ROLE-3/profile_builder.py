import os
import json
from pathlib import Path

PROFILE_DIR = "candidate_profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

def save_candidate_profile(profile_data: dict) -> str:
    """
    Saves a candidate profile into the shared JSON format.
    """
    candidate_name = profile_data.get("name", "unknown_candidate")
    filename = f"{candidate_name.lower().replace(' ', '_')}_profile.json"
    file_path = os.path.join(PROFILE_DIR, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=4)
        
    print(f"✅ Profile successfully saved to {file_path}")
    return file_path

def load_candidate_profile(candidate_name: str) -> dict:
    """
    Loads an existing candidate profile for Talent Check (Role 4) and Skill Matching (Role 5).
    """
    filename = f"{candidate_name.lower().replace(' ', '_')}_profile.json"
    file_path = os.path.join(PROFILE_DIR, filename)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Profile for {candidate_name} not found at {file_path}")
        
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    # Test sample profile entry
    sample_profile = {
        "name": "Ananya Rao",
        "email": "ananya.rao@example.com",
        "education": [
            {
                "degree": "B.Tech in Computer Science",
                "institution": "JSS University",
                "year": "2029"
            }
        ],
        "skills": [
            {
                "skill_name": "Python",
                "category_code": "COD",
                "evidence": "Built backend applications",
                "confidence": "high"
            }
        ],
        "hackathons": [],
        "internships": [],
        "certifications": [],
        "preferred_roles": ["Software Engineer"],
        "cv_file": "resume_skills/Ananya Rao_skills.json"
    }
    save_candidate_profile(sample_profile)