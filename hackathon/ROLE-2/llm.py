from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def call_gemini(prompt: str) -> str:
    """Calls Gemini model and returns the raw text response."""
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )
    return response.text.strip()