from typing import Dict, List, Any

# Simple keyword-based mapping to IPC sections using knowledge base


def map_to_legal_sections(text: str, references: Dict[str, Any]) -> List[Dict[str, Any]]:
    text_lower = (text or "").lower()
    results: List[Dict[str, Any]] = []

    # Hardcoded crime-to-IPC mapping for common cases
    crime_to_ipc = {
        "theft": {"code": "IPC 379", "title": "Theft", "description": "Punishment for theft"},
        "assault": {"code": "IPC 323", "title": "Assault", "description": "Punishment for voluntarily causing hurt"},
        "cheating": {"code": "IPC 420", "title": "Cheating", "description": "Cheating and dishonestly inducing delivery of property"},
        "murder": {"code": "IPC 302", "title": "Murder", "description": "Punishment for murder"},
        "robbery": {"code": "IPC 392", "title": "Robbery", "description": "Punishment for robbery"},
        "kidnapping": {"code": "IPC 363", "title": "Kidnapping", "description": "Punishment for kidnapping"},
        "rape": {"code": "IPC 376", "title": "Rape", "description": "Punishment for rape"},
    }
    
    # Threat-related keywords mapping to IPC 506 / BNS 351
    threat_keywords = ["threaten", "threat", "kill", "burn", "harm", "intimidate", "extort"]

    # Check for threat keywords and map to IPC 506 / BNS 351
    threat_detected = any(keyword in text_lower for keyword in threat_keywords)
    if threat_detected:
        matched_threat_keywords = [kw for kw in threat_keywords if kw in text_lower]
        results.append({
            "code": "IPC 506",
            "title": "Criminal Intimidation",
            "description": "Punishment for criminal intimidation",
            "matched_keywords": matched_threat_keywords,
        })
        results.append({
            "code": "BNS 351",
            "title": "Criminal Intimidation",
            "description": "Bharatiya Nyaya Sanhita - Punishment for criminal intimidation",
            "matched_keywords": matched_threat_keywords,
        })
    
    # Check for hardcoded mappings
    for crime, section_info in crime_to_ipc.items():
        if crime in text_lower:
            results.append({
                "code": section_info["code"],
                "title": section_info["title"],
                "description": section_info["description"],
                "matched_keywords": [crime],
            })

    # Then check knowledge base references
    for sec in references.get("sections", []):
        keywords = [k.lower() for k in sec.get("keywords", [])]
        if any(k in text_lower for k in keywords):
            # Avoid duplicates
            if not any(r["code"] == sec.get("code") for r in results):
                results.append({
                    "code": sec.get("code"),
                    "title": sec.get("title"),
                    "description": sec.get("description"),
                    "matched_keywords": [k for k in keywords if k in text_lower],
                })

    return results[:10]
