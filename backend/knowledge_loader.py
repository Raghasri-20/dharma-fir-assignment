import json
from pathlib import Path
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base" / "legal_knowledge.json"
LEGACY_KB_PATH = BASE_DIR / "knowledge_base" / "legal_reference.json"


def load_legal_knowledge() -> Dict[str, Any]:
    """Load legal_knowledge.json extracted from PDFs/PPTs"""
    print("📚 Loading legal knowledge base...")
    
    if KB_PATH.exists():
        try:
            with open(KB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                sections = data.get("legal_sections", [])
                print(f"✓ Knowledge base loaded: {len(sections)} legal sections")
                logger.info(f"Loaded {len(sections)} legal sections from knowledge base")
                return data
        except Exception as e:
            print(f"⚠️  Error loading knowledge base: {e}")
            logger.error(f"Error loading knowledge base: {e}")
            return {"legal_sections": [], "total_sections": 0}
    else:
        print(f"⚠️  Knowledge base not found at: {KB_PATH}")
        logger.warning(f"Knowledge base file not found: {KB_PATH}")
        return {"legal_sections": [], "total_sections": 0}


def format_legal_context(knowledge_base: Dict[str, Any], max_sections: int = 30) -> str:
    """Format legal sections into readable string for Gemini prompt"""
    sections = knowledge_base.get("legal_sections", [])
    
    if not sections:
        return "No legal context available."
    
    # Limit to max_sections to keep prompt size manageable
    sections_to_format = sections[:max_sections]
    
    formatted_lines = []
    for section in sections_to_format:
        section_num = section.get("section_number", "Unknown")
        title = section.get("title", "")
        explanation = section.get("explanation", "")
        
        # Format: "Section Number: Title — Explanation"
        formatted_lines.append(f"{section_num}: {title} — {explanation}")
    
    formatted_context = "\n".join(formatted_lines)
    
    if len(sections) > max_sections:
        formatted_context += f"\n... ({len(sections) - max_sections} more sections available)"
    
    print(f"✓ Formatted {len(sections_to_format)} sections for Gemini context (total: {len(sections)})")
    
    return formatted_context


def load_legal_references() -> Dict[str, Any]:
    """Legacy function for backward compatibility"""
    if LEGACY_KB_PATH.exists():
        with open(LEGACY_KB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"sections": []}
