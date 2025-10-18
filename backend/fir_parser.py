import re
from typing import Dict, List

# Very naive extraction heuristics for demo purposes
# You should replace with proper NER (spaCy/HF) for production use

def extract_entities(text: str) -> Dict[str, List[str]]:
    if not text:
        return {"names": [], "dates": [], "locations": [], "phone_numbers": [], "crimes": [], "objects": [], "threats": []}

    # Names: Contextual extraction to avoid false positives
    names: List[str] = []
    
    # Pattern 1: After keywords - extract proper names (1-3 words, flexible for single names)
    # Use word boundaries and ensure we're capturing actual names, not verbs
    name_context_patterns = [
        # Full names (2 words) with context
        r"(?:complainant|accused|witness|victim|suspect)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)(?:\s*,|\s+S/o|\s+D/o|\s+W/o|\s+reported|\s+stated)",
        r"(?:by|from)\s+accused\s+([A-Z][a-z]+\s+[A-Z][a-z]+)(?:\s+and|\s*,|\s*\.)",
        # Single or full names after "kill", "harm", "threaten" (for threat contexts)
        r"(?:kill|harm|murder|threaten)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)(?:\s+and|\s*,|\s*\.)",
        # Titles
        r"(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        # Relationships
        r"S/o\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",  # Son of
        r"D/o\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",  # Daughter of
        r"W/o\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",  # Wife of
        # Multiple accused
        r"\baccused\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+and\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",  # "accused Name1 and Name2"
    ]
    
    for pattern in name_context_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        # Handle tuples from patterns with multiple groups (e.g., "accused Name1 and Name2")
        for match in matches:
            if isinstance(match, tuple):
                names.extend([m for m in match if m])
            else:
                names.append(match)
    
    # Pattern 2: Capitalized words but filter out common false positives
    candidate_names = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b", text)
    
    # Filter out words that are likely not names
    stop_words = {
        "Stolen", "Theft", "Assault", "Police", "Station", "Road", "Street", "City",
        "State", "Country", "Date", "Time", "Place", "Location", "Incident", "Case",
        "Report", "Complaint", "Section", "Act", "Court", "Judge", "Lawyer",
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
        "January", "February", "March", "April", "May", "June", "July", "August",
        "September", "October", "November", "December", "Scheduled Caste",
        "Threatened To", "Saying I", "Will Kill", "Market Area", "Narsapur Road",
        "His Hut", "Her House", "Their Property"
    }
    
    # Additional verb patterns to exclude
    verb_patterns = [
        r"threatened\s+to",
        r"saying\s+",
        r"will\s+",
        r"fled\s+towards",
    ]
    
    for name in candidate_names:
        # Check if it's not a stop word and not starting a sentence after period
        words = name.split()
        name_lower = name.lower()
        
        # Skip if contains stop words
        if any(word in stop_words for word in words):
            continue
        
        # Skip if matches verb patterns
        if any(re.search(pattern, name_lower) for pattern in verb_patterns):
            continue
        
        # Skip possessive phrases (his/her/their)
        if re.match(r"^(his|her|their)\s+", name_lower):
            continue
            
        # Only add multi-word names
        if len(words) >= 2:
            names.append(name)

    # Dates: Enhanced patterns including written dates
    dates: List[str] = []
    date_patterns = [
        r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",  # 12/09/2024
        r"\b\d{4}-\d{2}-\d{2}\b",  # 2024-09-12
        r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b",  # 14th September 2025
        r"\bon\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",  # on 12/09/2024
        r"\bdate[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",  # date: 12/09/2024
    ]
    
    for pat in date_patterns:
        matches = re.findall(pat, text, flags=re.IGNORECASE)
        dates.extend(matches)

    # Locations: Enhanced patterns with better context
    locations: List[str] = []
    location_patterns = [
        r"(?:at|in|near|around|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}(?:\s+(?:Road|Street|Avenue|Lane|Circle|Market|Nagar|Colony|Area|Chowk|Crossing)))",  # near Narsapur Road
        r"(?:at|in|near)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b(?!\s+(?:was|were|is|are|has|have|said|told))",  # General location after at/in/near
        r"(?:place|location|address)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,4})",  # place: Location Name
        r"resident of\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,4})",  # resident of
        r"R/o\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,4})",  # R/o (Resident of)
        r"(?:village|city|town|district)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})",  # village/city/town
    ]
    
    for pattern in location_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        locations.extend(matches)

    # Indian phone numbers (10 digits)
    phones = re.findall(r"\b[6-9]\d{9}\b", text)

    # Crimes: keyword matching
    crime_keywords = {
        "theft": r"\b(theft|stole|stolen|steal|stealing)\b",
        "assault": r"\b(assault|assaulted|attacked|beating|hit)\b",
        "cheating": r"\b(cheat|cheated|fraud|deceive)\b",
        "murder": r"\b(murder|killed|killing)\b",
        "robbery": r"\b(robbery|robbed|looted)\b",
        "kidnapping": r"\b(kidnap|kidnapped|abduct)\b",
        "rape": r"\b(rape|raped|sexual assault)\b",
    }
    crimes: List[str] = []
    for crime, pattern in crime_keywords.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            crimes.append(crime)

    # Objects: common items mentioned in FIRs
    object_keywords = [
        r"\b(mobile|phone|smartphone)\b",
        r"\b(cash|money|rupees|Rs\.?\s*\d+)\b",
        r"\b(jewellery|gold|silver|ornaments)\b",
        r"\b(wallet|purse|bag)\b",
        r"\b(laptop|computer|tablet)\b",
        r"\b(vehicle|car|bike|motorcycle|scooter)\b",
        r"\b(documents|papers|certificates)\b",
        r"\b(weapon|knife|gun|pistol)\b",
    ]
    objects: List[str] = []
    for pattern in object_keywords:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        objects.extend(matches)

    # Threats: keyword matching for threatening behavior
    threat_keywords = {
        "kill": r"\b(kill|killed|killing|murder)\b",
        "burn": r"\b(burn|burned|burning|set fire)\b",
        "harm": r"\b(harm|hurt|injure|damage)\b",
        "threaten": r"\b(threaten|threatened|threatening|threat)\b",
        "intimidate": r"\b(intimidate|intimidated|intimidation)\b",
        "extort": r"\b(extort|extortion|blackmail)\b",
        "assault": r"\b(assault|attack|beat)\b",
    }
    threats: List[str] = []
    for threat_type, pattern in threat_keywords.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            threats.append(threat_type)

    # Basic cleanup & uniqueness
    def uniq(xs: List[str]) -> List[str]:
        seen = set()
        out: List[str] = []
        for x in xs:
            cleaned = x.strip()
            if cleaned and cleaned not in seen:
                out.append(cleaned)
                seen.add(cleaned)
        return out
    
    # Additional cleanup for names - remove any that are substrings of locations
    cleaned_names = []
    location_set = set(loc.lower() for loc in locations)
    for name in names:
        # Don't add if it's part of a location
        if not any(name.lower() in loc for loc in location_set):
            cleaned_names.append(name)

    return {
        "names": uniq(cleaned_names)[:10],
        "dates": uniq(dates)[:10],
        "locations": uniq(locations)[:10],
        "phone_numbers": uniq(phones)[:10],
        "crimes": uniq([c.lower() for c in crimes]),
        "objects": uniq([o.lower() for o in objects])[:10],
        "threats": uniq([t.lower() for t in threats]),
    }

# ---------------------- Regex-based structured extractors ----------------------

def extract_complainant(text: str) -> Dict[str, object]:
    complainant: Dict[str, object] = {}
    # Name, Father, Age
    m = re.search(r"complainant\s+(.*?)\s*,\s*S/o\s+(.*?),\s*aged\s*(\d+)", text, flags=re.IGNORECASE | re.DOTALL)
    if m:
        complainant["Name"] = m.group(1).strip()
        complainant["Father"] = m.group(2).strip()
        try:
            complainant["Age"] = int(m.group(3))
        except ValueError:
            pass

    if re.search(r"\bScheduled\s+Caste\b", text, flags=re.IGNORECASE):
        complainant["Community"] = "Scheduled Caste"

    occ = re.search(r"occupation:\s*(.*?)(?:,|\.|\n)", text, flags=re.IGNORECASE)
    if occ:
        complainant["Occupation"] = occ.group(1).strip()

    addr = re.search(r"resident of\s+(.*?)(?:,|\.|\n)", text, flags=re.IGNORECASE)
    if addr:
        complainant["Address"] = addr.group(1).strip()

    contact = re.search(r"contact\s*[:\-]\s*([+]?\d[\d\- ]{7,}\d)", text, flags=re.IGNORECASE)
    if contact:
        complainant["Contact"] = contact.group(1).strip()

    return complainant


def extract_datetime(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    # Date and time patterns
    date = re.search(r"\b(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}-\d{2}-\d{2})\b", text)
    if date:
        out["Date"] = date.group(1)
    time = re.search(r"\b(\d{1,2}\s*(?:AM|PM)|\d{1,2}:\d{2}\s*(?:AM|PM)?|\d{1,2}\s*o'?clock)\b", text, flags=re.IGNORECASE)
    if time:
        out["Time"] = time.group(1)
    datetime_phrase = re.search(r"on\s+(.*?)\s+at\s+(\d{1,2}[:\.]?\d{0,2}\s*(?:AM|PM)?)", text, flags=re.IGNORECASE)
    if datetime_phrase and "Date" not in out:
        out["Phrase"] = datetime_phrase.group(0)
    return out


def extract_place(text: str) -> Dict[str, str]:
    place: Dict[str, str] = {}
    # Try landmark or area after 'at'/'in'
    at_in = re.search(r"\b(?:at|in)\s+([A-Z][\w\-]*(?:\s+[A-Z][\w\-]*){0,4})\b", text)
    if at_in:
        place["Location"] = at_in.group(1).strip()
    addr = re.search(r"address\s*[:\-]\s*(.*?)(?:\.|\n)", text, flags=re.IGNORECASE)
    if addr:
        place["Address"] = addr.group(1).strip()
    ps = re.search(r"police\s*station\s*[:\-]?\s*([A-Za-z ]+)", text, flags=re.IGNORECASE)
    if ps:
        place["PoliceStation"] = ps.group(1).strip()
    city = re.search(r"\bcity\s*[:\-]\s*([A-Za-z ]+)", text, flags=re.IGNORECASE)
    if city:
        place["City"] = city.group(1).strip()
    return place


def extract_accused_list(text: str) -> List[Dict[str, str]]:
    accused: List[Dict[str, str]] = []
    # Patterns like Accused: Name S/o Father, R/o Address ...; multiple names separated by commas
    block = re.search(r"accused\s*[:\-]\s*(.*)", text, flags=re.IGNORECASE)
    if block:
        names = re.split(r"[,;]\s*", block.group(1))
        for n in names:
            n = n.strip()
            if not n:
                continue
            entry: Dict[str, str] = {"Raw": n}
            m = re.search(r"^(.*?)\s*(?:S/o\s*(.*?))?(?:,|$)", n, flags=re.IGNORECASE)
            if m:
                if m.group(1):
                    entry["Name"] = m.group(1).strip()
                if m.group(2):
                    entry["Father"] = m.group(2).strip()
            addr = re.search(r"R/o\s*(.*)", n, flags=re.IGNORECASE)
            if addr:
                entry["Address"] = addr.group(1).strip()
            if entry:
                accused.append(entry)
    # Also capture "unknown persons" type
    if not accused and re.search(r"unknown\s+person", text, flags=re.IGNORECASE):
        accused.append({"Name": "Unknown persons"})
    return accused


def extract_vehicles(text: str) -> List[Dict[str, str]]:
    vehicles: List[Dict[str, str]] = []
    # Registration numbers: e.g., DL 01 AB 1234, KA-05-1234
    for m in re.finditer(r"\b[A-Z]{2}[- ]?\d{1,2}[ -]?[A-Z]{1,2}[ -]?\d{3,4}\b", text):
        vehicles.append({"Registration": m.group(0)})
    # Vehicle mentions
    for m in re.finditer(r"\b(car|bike|motorcycle|scooter|auto|truck|bus)\b", text, flags=re.IGNORECASE):
        vehicles.append({"Type": m.group(1)})
    return vehicles


def extract_weapons(text: str) -> List[str]:
    weapons: List[str] = []
    keywords = [
        r"knife", r"dagger", r"pistol", r"revolver", r"gun", r"rifle", r"rod", r"stick",
        r"lathi", r"machete"
    ]
    for kw in keywords:
        for _ in re.finditer(rf"\b{kw}\b", text, flags=re.IGNORECASE):
            weapons.append(kw)
    return list(dict.fromkeys(weapons))


def extract_injuries(text: str) -> List[str]:
    injuries: List[str] = []
    patterns = [r"injur(?:y|ies)", r"bleeding", r"fracture", r"bruise", r"laceration", r"hurt"]
    for p in patterns:
        for _ in re.finditer(rf"\b{p}\b", text, flags=re.IGNORECASE):
            injuries.append(p)
    return list(dict.fromkeys(injuries))


def extract_threats(text: str) -> List[str]:
    threats: List[str] = []
    threat_map = {
        "threaten": r"\b(?:threaten(?:ed|ing)?|threat)\b",
        "intimidate": r"\b(?:intimidat(?:e|ed|ing|ion))\b",
        "extort": r"\b(?:extort(?:ion)?|blackmail)\b",
    }
    for threat_name, pattern in threat_map.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            threats.append(threat_name)
    return threats


def extract_witnesses(text: str) -> List[Dict[str, str]]:
    witnesses: List[Dict[str, str]] = []
    # Look for witness names after keywords - capture full names with titles
    for m in re.finditer(r"witness\s+(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", text, flags=re.IGNORECASE):
        name = m.group(1).strip()
        if name and len(name) > 2:  # Avoid capturing just "Mr"
            witnesses.append({"Name": name})
    # Also capture phrases like "in presence of <Name>"
    for m in re.finditer(r"in\s+presence\s+of\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", text):
        name = m.group(1).strip()
        if name:
            witnesses.append({"Name": name})
    return witnesses


def extract_property_loss(text: str) -> Dict[str, str]:
    loss: Dict[str, str] = {}
    # Monetary amounts
    amt = re.search(r"(?:Rs\.?|INR)\s*([0-9,]+)\b", text, flags=re.IGNORECASE)
    if amt:
        loss["Amount"] = amt.group(1).replace(",", "")
    # Items lost
    items = re.search(r"(mobile|cash|jewellery|gold|wallet|laptop|documents|property)", text, flags=re.IGNORECASE)
    if items:
        loss["Items"] = items.group(1)
    return loss


def parse_fir(text: str) -> Dict[str, object]:
    """Aggregate parser returning a structured dict of extracted fields."""
    return {
        "complainant": extract_complainant(text),
        "datetime": extract_datetime(text),
        "place": extract_place(text),
        "accused": extract_accused_list(text),
        "vehicles": extract_vehicles(text),
        "weapons": extract_weapons(text),
        "injuries": extract_injuries(text),
        "threats": extract_threats(text),
        "witnesses": extract_witnesses(text),
        "property_loss": extract_property_loss(text),
    }
