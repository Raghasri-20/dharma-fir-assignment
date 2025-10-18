from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
import logging

from fir_parser import parse_fir
from legal_mapper import map_to_legal_sections
from summarizer import summarize_text
from knowledge_loader import load_legal_references, load_legal_knowledge, format_legal_context
from gemini_extractor import get_gemini_extractor
from gemini_legal_mapper import create_gemini_legal_mapper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load legal knowledge base at startup
print("\n" + "="*70)
print("INITIALIZING DHARMA FIR API")
print("="*70)
LEGAL_KNOWLEDGE = load_legal_knowledge()
LEGAL_CONTEXT = format_legal_context(LEGAL_KNOWLEDGE, max_sections=25)  # Limit to 25 sections
print("="*70 + "\n")


class FIRRequest(BaseModel):
    text: str


app = FastAPI(title="Dharma FIR API", version="0.1.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> Dict[str, Any]:
    return {"status": "ok", "service": "dharma-fir", "version": "0.1.0"}


@app.post("/process")
def process_fir(req: FIRRequest) -> Dict[str, Any]:
    text = req.text or ""
    
    # Extract entities using Gemini (no fallback)
    gemini_extractor = get_gemini_extractor()
    
    try:
        entities = gemini_extractor.extract_entities(text)
        logger.info("Successfully extracted entities using Gemini")
    except Exception as e:
        logger.error(f"Gemini extraction failed: {e}")
        return {
            "error": "Entity extraction failed",
            "message": str(e),
            "entities": None,
            "legal_sections": [],
            "summary": "",
        }
    
    refs = load_legal_references()
    legal_sections = map_to_legal_sections(text, refs)
    summary = summarize_text(text, entities, legal_sections)

    return {
        "entities": entities,
        "legal_sections": legal_sections,
        "summary": summary,
        "references": refs,
        "extraction_method": "gemini",
    }


@app.post("/parse-fir")
def parse_fir_endpoint(req: FIRRequest) -> Dict[str, Any]:
    text = req.text or ""
    
    print("\n" + "="*70)
    print("PROCESSING FIR REQUEST")
    print("="*70)
    print(f"FIR text length: {len(text)} characters")
    
    # Extract entities using Gemini (no fallback)
    print("\n🤖 Step 1: Entity Extraction")
    gemini_extractor = get_gemini_extractor()
    
    try:
        entities = gemini_extractor.extract_entities(text)
        print("✓ Entity extraction complete")
        logger.info("Successfully extracted entities using Gemini")
    except Exception as e:
        print(f"❌ Entity extraction failed: {e}")
        logger.error(f"Gemini extraction failed: {e}")
        return {
            "error": "Entity extraction failed",
            "message": str(e),
            "entities": None,
            "legal_sections": [],
            "summary": "",
        }
    
    # Map to legal sections using Gemini with knowledge base
    print("\n⚖️  Step 2: Legal Section Mapping")
    try:
        legal_mapper = create_gemini_legal_mapper(gemini_extractor.model)
        legal_sections = legal_mapper.map_to_legal_sections(text, entities, LEGAL_CONTEXT)
        print("✓ Legal mapping complete")
    except Exception as e:
        print(f"❌ Legal mapping failed: {e}")
        logger.error(f"Legal mapping failed: {e}")
        legal_sections = []
    
    # Generate summary
    print("\n📝 Step 3: Summary Generation")
    summary = summarize_text(text, entities, legal_sections)
    print("✓ Summary generated")
    
    print("\n" + "="*70)
    print("✓ FIR PROCESSING COMPLETE")
    print("="*70 + "\n")

    return {
        "entities": entities,
        "legal_sections": legal_sections,
        "summary": summary,
        "extraction_method": "gemini-2.5-flash",
        "total_sections_in_kb": LEGAL_KNOWLEDGE.get("total_sections", 0),
    }
