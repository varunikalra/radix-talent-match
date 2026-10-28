import os
import json
import glob

VALID_CATEGORIES = {"COD", "DSA", "OOD", "COMM", "AI", "APTI", "CLOUD", "SYSD", "SQL", "SWE", "NETW", "OS", "OTHER"}
OUTPUT_DIR = "resume_skills"

def validate_json_files():
    files = glob.glob(os.path.join(OUTPUT_DIR, "*_skills.json"))
    if not files:
        print("No parsed resume JSON files found to validate yet.")
        return

    for file_path in files:
        print(f"Validating {os.path.basename(file_path)}...")
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Error: {file_path} is not valid JSON.")
                continue

        # Check required keys
        required_keys = {"source_type", "source_file", "candidate_name", "skills"}
        if not required_keys.issubset(data.keys()):
            print(f"❌ Error: Missing top-level keys in {file_path}")
            continue

        # Validate each skill category
        invalid_categories = []
        for skill in data.get("skills", []):
            cat = skill.get("category_code")
            if cat not in VALID_CATEGORIES:
                invalid_categories.append((skill.get("skill_name"), cat))

        if invalid_categories:
            print(f"⚠️ Warning: Invalid categories found in {file_path}: {invalid_categories}")
        else:
            print(f"✅ {os.path.basename(file_path)} passed validation successfully!")

if __name__ == "__main__":
    validate_json_files()