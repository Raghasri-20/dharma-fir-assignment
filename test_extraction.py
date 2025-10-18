"""
Quick test script for legal knowledge extraction
Creates a sample text file and tests the extraction logic
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from dotenv import load_dotenv
import google.generativeai as genai
import json

print("=" * 70)
print("TESTING GEMINI EXTRACTION")
print("=" * 70)

# Load API key
backend_dir = Path(__file__).parent / "backend"
env_path = backend_dir / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"✓ Loaded .env from: {env_path}")
else:
    print("❌ .env file not found")
    sys.exit(1)

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found")
    sys.exit(1)

print(f"✓ API key found: {api_key[:20]}...")

# Configure Gemini
genai.configure(api_key=api_key, transport="rest")
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
print("✓ Gemini 2.5 Flash initialized")

# Test text with legal sections
test_text = """
IPC Section 302 deals with Murder. Whoever commits murder shall be punished 
with death or imprisonment for life, and shall also be liable to fine.

IPC Section 304 covers Culpable Homicide Not Amounting to Murder. Whoever 
commits culpable homicide not amounting to murder shall be punished with 
imprisonment for life, or imprisonment for a term which may extend to ten years.

CrPC Section 154 mandates that every information relating to the commission 
of a cognizable offense, if given orally to an officer in charge of a police 
station, shall be reduced to writing by him or under his direction.
"""

print("\n" + "=" * 70)
print("TEST TEXT")
print("=" * 70)
print(test_text[:200] + "...")

# Create prompt
prompt = f"""You are a legal expert analyzing Indian legal documents. Extract all legal sections mentioned in the following text.

Text:
{test_text}

Return a JSON array of legal sections with the following structure:
[
  {{
    "section_number": "IPC Section 302",
    "title": "Murder",
    "explanation": "Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine."
  }}
]

Rules:
1. Extract ALL legal sections mentioned (IPC, CrPC, etc.)
2. Include the full section number (e.g., "IPC Section 302", "CrPC Section 154")
3. Provide a clear title for each section
4. Give a concise explanation of what the section covers
5. Return ONLY the JSON array, no additional text
6. If no legal sections are found, return an empty array: []

Return the JSON array now:"""

print("\n🤖 Sending to Gemini...")

try:
    response = model.generate_content([prompt])
    print("✓ Response received")
    
    if response and response.text:
        # Parse response
        response_text = response.text.strip()
        
        # Remove markdown
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        sections = json.loads(response_text)
        
        print("\n" + "=" * 70)
        print("EXTRACTED SECTIONS")
        print("=" * 70)
        print(json.dumps(sections, indent=2))
        
        print("\n" + "=" * 70)
        print(f"✓ TEST SUCCESSFUL! Extracted {len(sections)} sections")
        print("=" * 70)
        
    else:
        print("❌ Empty response from Gemini")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
