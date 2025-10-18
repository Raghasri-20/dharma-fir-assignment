"""Test short threat sentence"""
import sys
sys.path.insert(0, '.')

from backend.fir_parser import extract_entities
from backend.legal_mapper import map_to_legal_sections
from backend.summarizer import summarize_text
from backend.knowledge_loader import load_legal_references

# Your test case
test_text = "He threatened to kill Ramu and burn his hut."

print("Input:", test_text)
print("=" * 60)

entities = extract_entities(test_text)
refs = load_legal_references()
legal_sections = map_to_legal_sections(test_text, refs)
summary = summarize_text(test_text, entities, legal_sections)

print("\n📋 ENTITIES:")
print(f"  Names: {entities['names']}")
print(f"  Threats: {entities['threats']}")
print(f"  Crimes: {entities['crimes']}")
print(f"  Objects: {entities['objects']}")

print("\n⚖️  LEGAL SECTIONS:")
for sec in legal_sections:
    print(f"  • {sec['code']}: {sec['title']}")

print("\n📝 SUMMARY:")
print(f"  {summary}")

print("\n" + "=" * 60)
print("✓ Expected: Name 'Ramu', Threats: threaten, kill, burn")
print("✓ Expected: Sections IPC 506, BNS 351")
