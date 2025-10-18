"""Gemini AI integration for FIR entity extraction using google-generativeai SDK"""
import os
import json
import logging
from typing import Dict, List
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiExtractor:
    """Extract entities from FIR text using Gemini AI"""
    
    def __init__(self):
        self.model = None
        self.initialized = False
        
        try:
            # Load environment variables from .env file
            backend_dir = Path(__file__).parent
            env_path = backend_dir / ".env"
            
            if env_path.exists():
                load_dotenv(dotenv_path=env_path)
            else:
                load_dotenv()  # Try loading from default locations
            
            # Get API key from environment
            api_key = os.environ.get("GOOGLE_API_KEY")
            
            if not api_key:
                logger.error("GOOGLE_API_KEY not found in environment")
                return
            
            # Configure Gemini with REST transport (not gRPC)
            genai.configure(
                api_key=api_key,
                transport="rest"  # Force REST API instead of gRPC
            )
            
            # Initialize Gemini model - using stable Gemini 2.5 Flash
            self.model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
            self.initialized = True
            logger.info("Gemini AI initialized successfully with gemini-2.5-flash (REST)")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {e}")
            self.initialized = False
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities using Gemini.
        Raises exception if extraction fails.
        """
        if not self.initialized or not self.model:
            raise RuntimeError("Gemini not initialized. Check GOOGLE_API_KEY in .env file.")
        
        if not text or not text.strip():
            raise ValueError("Empty FIR text provided")
        
        prompt = f"""You are a legal assistant. Extract structured entities from the following FIR text.

FIR:
{text}

Return a JSON with keys: names, dates, locations, phone_numbers, crimes, threats, objects.

Example output:
{{
  "names": ["Ramu"],
  "dates": ["14th September 2025"],
  "locations": ["Narsapur"],
  "phone_numbers": [],
  "crimes": ["theft"],
  "threats": ["kill"],
  "objects": ["bike"]
}}
"""

        try:
            # Generate response (pass prompt as list)
            response = self.model.generate_content([prompt])
            
            if not response or not response.text:
                raise RuntimeError("Empty response from Gemini")
            
            # Parse JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            entities = json.loads(response_text)
            
            # Validate structure
            required_keys = ["names", "dates", "locations", "phone_numbers", "crimes", "threats", "objects"]
            if not all(key in entities for key in required_keys):
                raise ValueError(f"Gemini response missing required keys. Got: {list(entities.keys())}")
            
            # Ensure all values are lists
            for key in required_keys:
                if not isinstance(entities[key], list):
                    entities[key] = []
            
            logger.info(f"Successfully extracted entities: {len(entities.get('names', []))} names, "
                       f"{len(entities.get('crimes', []))} crimes, {len(entities.get('threats', []))} threats")
            
            return entities
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini JSON response: {e}")
            logger.error(f"Response text: {response.text if response else 'None'}")
            raise RuntimeError(f"Invalid JSON response from Gemini: {e}")
        except Exception as e:
            logger.error(f"Gemini extraction failed: {e}")
            raise


# Global instance
_gemini_extractor = None

def get_gemini_extractor() -> GeminiExtractor:
    """Get or create global Gemini extractor instance"""
    global _gemini_extractor
    if _gemini_extractor is None:
        _gemini_extractor = GeminiExtractor()
    return _gemini_extractor
