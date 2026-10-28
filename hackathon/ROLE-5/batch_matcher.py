import os
import json
from skill_matcher import compute_skill_match

candidates = [
    "Ananya Rao",
    "Karthik Subramaniam",
    "Priya Menon",
    "Rohan Verma"
]

def run_all_matches():
    print(f"🎯 Running skill matching for {len(candidates)} candidates...\n")
    for name in candidates:
        try:
            compute_skill_match(name)
        except Exception as e:
            print(f"❌ Error processing {name}: {e}")

if __name__ == "__main__":
    run_all_matches()