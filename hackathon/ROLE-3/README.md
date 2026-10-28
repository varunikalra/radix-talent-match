
# Role 3: Profile Builder (RADIX Talent Match)

The Profile Builder module allows candidates to build and manage their comprehensive profiles—incorporating basic details, education, hackathons, internships, certifications, preferred roles, and pre-filling skills extracted from Role 2 (Resume Parsing).

## 📂 Folder Structure

- `candidate_profiles/`: Stores generated and saved candidate profiles in JSON format.
- `profile_builder.py`: Core profile creation and loading utility.
- `generate_all_profiles.py`: Batch generator script for sample hackathon candidates.
- `api.py`: FastAPI backend endpoints for profile submission and retrieval.
- `validate_output.py`: Schema validation script checking profiles against the RADIX contract.

## 🚀 Getting Started

1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
