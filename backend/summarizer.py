from typing import Dict, List

# Heuristic summary placeholder; integrate LLM as needed

def summarize_text(text: str, entities: Dict[str, List[str]], legal_sections: List[Dict]) -> str:
    if not text:
        return "No FIR text provided."

    parts: List[str] = []
    
    # Format: "Potential applicable sections: IPC 379 - Theft; IPC 323 - Assault"
    if legal_sections:
        section_strs = [f"{s.get('code')} - {s.get('title')}" for s in legal_sections]
        parts.append("Potential applicable sections: " + "; ".join(section_strs))
    
    # Format: "Mentioned names: Ramu, Shyam"
    if entities.get("names"):
        parts.append("Mentioned names: " + ", ".join(entities["names"][:5]))
    
    # Add crimes if detected
    if entities.get("crimes"):
        parts.append("Crimes detected: " + ", ".join(entities["crimes"]))
    
    # Add threats if detected
    if entities.get("threats"):
        parts.append("Threats detected: " + ", ".join(entities["threats"]))
    
    # Add objects if detected
    if entities.get("objects"):
        parts.append("Objects involved: " + ", ".join(entities["objects"][:5]))
    
    # Add locations
    if entities.get("locations"):
        parts.append("Locations: " + ", ".join(entities["locations"][:3]))
    
    # Add dates
    if entities.get("dates"):
        parts.append("Dates: " + ", ".join(entities["dates"][:3]))

    if not parts:
        parts.append("No salient entities or sections detected.")

    return ". ".join(parts) + "."
