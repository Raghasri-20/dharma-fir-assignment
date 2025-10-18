import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
genai.configure(api_key="AIzaSyARcJWEONItPINU_n1-rQM5njUk-Q8KmOk")

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-pro")

# Prompt for FIR entity extraction
prompt = """
Extract structured FIR entities from the following text:
He threatened to kill Ramu and burn his hut.

Return a JSON with keys: names, dates, locations, phone_numbers, crimes, threats, objects.
"""

# Gemini expects a list of content parts
response = model.generate_content([prompt])

# Print the output
print("Gemini Output:\n", response.text)