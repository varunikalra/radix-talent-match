import os
import json

VALID_CATEGORIES = {"COD", "DSA", "OOD", "COMM", "AI", "APTI", "CLOUD", "SYSD", "SQL", "SWE", "NETW", "OS", "OTHER"}

def validate_jsons():
    json_files = os.listdir("jd_skills")
    json_files = [f for f in json_files if f.endswith(".json")]
    
    if not json_files:
        print("No JSON files found in 'jd_skills/' to validate.")
        return

    print(f"Validating {len(json_files)} extracted job description file(s)...\n")
    
    all_valid = True
    for file in json_files:
        path = os.path.join("jd_skills", file)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Check required keys
            assert "source_file" in data, "Missing 'source_file'"
            assert "skills" in data, "Missing 'skills' list"
            
            # Check category codes
            for idx, skill in enumerate(data["skills"]):
                cat = skill.get("category_code")
                if cat not in VALID_CATEGORIES:
                    print(f"❌ [{file}] Skill #{idx+1} ('{skill.get('skill_name')}') has invalid category: '{cat}'")
                    all_valid = False
                    
            print(f"✅ {file}: Valid structure and categories.")
        except Exception as e:
            print(f"❌ {file}: Validation error -> {e}")
            all_valid = False
            
    if all_valid:
        print("\n🎉 All Role 1 JSON files are fully validated and ready!")
    else:
        print("\n⚠️ Some files need review.")

if __name__ == "__main__":
    validate_jsons()