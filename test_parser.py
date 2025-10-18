"""Quick test script to verify FIR parser functionality"""
from backend.fir_parser import extract_entities, parse_fir
from backend.legal_mapper import map_to_legal_sections
from backend.summarizer import summarize_text
from backend.knowledge_loader import load_legal_references
import json

# Test case 1: Comprehensive FIR
test_fir_1 = """
On 14th September 2025, complainant Rahul Verma, S/o Ramesh Verma, reported that he was 
assaulted and his mobile phone was stolen near Narsapur Road by accused Ramu Singh and 
Shyam Kumar. The incident took place at around 3 PM. Witness Mr. Prakash Sharma was present. 
The accused threatened the victim saying "I will kill you and burn your house" and fled 
towards Market Area. Contact: 9876543210.
"""

# Test case 2: Only threats
test_fir_2 = """
The accused threatened to kill and burn the victim.
"""

print("=" * 80)
print("TEST CASE 1: Comprehensive FIR")
print("=" * 80)

entities_1 = extract_entities(test_fir_1)
refs = load_legal_references()
legal_sections_1 = map_to_legal_sections(test_fir_1, refs)
summary_1 = summarize_text(test_fir_1, entities_1, legal_sections_1)

print("\n📋 ENTITIES:")
print(json.dumps(entities_1, indent=2))

print("\n⚖️  LEGAL SECTIONS:")
for sec in legal_sections_1:
    print(f"  • {sec['code']}: {sec['title']}")
    print(f"    Matched: {', '.join(sec['matched_keywords'])}")

print("\n📝 SUMMARY:")
print(summary_1)

print("\n" + "=" * 80)
print("TEST CASE 2: Only Threats")
print("=" * 80)

entities_2 = extract_entities(test_fir_2)
legal_sections_2 = map_to_legal_sections(test_fir_2, refs)
summary_2 = summarize_text(test_fir_2, entities_2, legal_sections_2)

print("\n📋 ENTITIES:")
print(json.dumps(entities_2, indent=2))

print("\n⚖️  LEGAL SECTIONS:")
for sec in legal_sections_2:
    print(f"  • {sec['code']}: {sec['title']}")
    print(f"    Matched: {', '.join(sec['matched_keywords'])}")

print("\n📝 SUMMARY:")
print(summary_2)

print("\n" + "=" * 80)
print("TEST CASE 3: Parsed Structure")
print("=" * 80)

parsed = parse_fir(test_fir_1)
print("\n🔍 PARSED DATA:")
print(json.dumps(parsed, indent=2))
