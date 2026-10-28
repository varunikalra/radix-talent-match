import os
import json

PROFILE_DIR = "candidate_profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

# Sample candidate dataset mapped from the hackathon brief
candidates = [
    {
        "name": "Ananya Rao",
        "email": "ananya.rao@example.com",
        "education": [{"degree": "B.Tech in Computer Science", "institution": "JSS University", "year": "2029"}],
        "skills": [{"skill_name": "Python", "category_code": "COD", "evidence": "Built backend applications", "confidence": "high"}],
        "hackathons": [{"event": "RADIX Hackathon", "project": "Placement Intelligence Hub", "year": "2026"}],
        "internships": [],
        "certifications": [],
        "preferred_roles": ["Software Engineer (SWE)"],
        "cv_file": "resume_skills/Ananya Rao_skills.json"
    },
    {
        "name": "Karthik Subramaniam",
        "email": "karthik.subramaniam@example.com",
        "education": [{"degree": "B.Tech in Data Science", "institution": "JSS University", "year": "2029"}],
        "skills": [{"skill_name": "Data Analytics", "category_code": "AI", "evidence": "Machine learning pipelines", "confidence": "high"}],
        "hackathons": [],
        "internships": [{"company": "DataCorp", "role": "Analyst Intern", "year": "2026"}],
        "certifications": [],
        "preferred_roles": ["Data Scientist", "Data Analyst"],
        "cv_file": "resume_skills/Karthik Subramaniam_skills.json"
    },
    {
        "name": "Priya Menon",
        "email": "priya.menon@example.com",
        "education": [{"degree": "B.Tech in Information Technology", "institution": "JSS University", "year": "2029"}],
        "skills": [{"skill_name": "System Support", "category_code": "OS", "evidence": "Technical troubleshooting", "confidence": "medium"}],
        "hackathons": [],
        "internships": [],
        "certifications": [{"title": "IT Support Professional", "year": "2026"}],
        "preferred_roles": ["Application Support Analyst"],
        "cv_file": "resume_skills/Priya Menon_skills.json"
    },
    {
        "name": "Rohan Verma",
        "email": "rohan.verma@example.com",
        "education": [{"degree": "B.Tech in Computer Science", "institution": "JSS University", "year": "2029"}],
        "skills": [{"skill_name": "Full Stack Development", "category_code": "COD", "evidence": "All-rounder projects", "confidence": "high"}],
        "hackathons": [{"event": "TGL Blitz", "project": "Fullstack Platform", "year": "2026"}],
        "internships": [{"company": "TechStart", "role": "SWE Intern", "year": "2026"}],
        "certifications": [],
        "preferred_roles": ["Software Engineer", "Data Scientist"],
        "cv_file": "resume_skills/Rohan Verma_skills.json"
    }
]

def generate_all():
    for candidate in candidates:
        name = candidate["name"]
        filename = f"{name.lower().replace(' ', '_')}_profile.json"
        file_path = os.path.join(PROFILE_DIR, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(candidate, f, indent=4)
        print(f"✅ Generated profile for {name}")

if __name__ == "__main__":
    generate_all()