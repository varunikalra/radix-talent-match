import os
import json

PROFILE_DIR = "candidate_profiles"
VALID_CATEGORIES = {
    "COD", "DSA", "OOD", "AI", "APTI", "COMM", 
    "CLOUD", "SYSD", "SOL", "SWE", "NETW", "OS", "OTHER"
}

def validate_profiles():
    if not os.path.exists(PROFILE_DIR):
        print(f"❌ Error: {PROFILE_DIR} directory does not exist.")
        return

    files = [f for f in os.listdir(PROFILE_DIR) if f.endswith(".json")]
    
    if not files:
        print("⚠️ No profile JSON files found to validate.")
        return

    print(f"🔍 Validating {len(files)} candidate profile(s)...\n")
    all_valid = True

    for file in files:
        file_path = os.path.join(PROFILE_DIR, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Check required top-level fields
            if "name" not in data or "email" not in data:
                print(f"❌ {file}: Missing required 'name' or 'email' field.")
                all_valid = False
                continue

            # Validate skill categories against the 12 RADIX codes
            file_skills_valid = True
            for skill in data.get("skills", []):
                cat = skill.get("category_code")
                if cat not in VALID_CATEGORIES:
                    print(f"⚠️ {file}: Invalid category code '{cat}' found in skill '{skill.get('skill_name')}'")
                    file_skills_valid = False

            if file_skills_valid:
                print(f"✅ {file}: Validated successfully.")
                
        except Exception as e:
            print(f"❌ {file}: Failed to parse JSON. Error: {e}")
            all_valid = False

    if all_valid:
        print("\n🎉 All candidate profiles passed validation successfully!")
    else:
        print("\n⚠️ Some profiles have validation warnings or errors.")

if __name__ == "__main__":
    validate_profiles()