"""
Test script for Gemini-based legal mapping with knowledge base
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from knowledge_loader import load_legal_knowledge, format_legal_context
from gemini_extractor import get_gemini_extractor
from gemini_legal_mapper import create_gemini_legal_mapper
import json

print("=" * 70)
print("TESTING GEMINI LEGAL MAPPING WITH KNOWLEDGE BASE")
print("=" * 70)

# Step 1: Load knowledge base
print("\n📚 Step 1: Loading Knowledge Base")
knowledge_base = load_legal_knowledge()
legal_context = format_legal_context(knowledge_base)

print(f"\nKnowledge base stats:")
print(f"  Total sections: {knowledge_base.get('total_sections', 0)}")
print(f"  Context length: {len(legal_context)} characters")
print(f"\nFirst 3 sections:")
for line in legal_context.split('\n')[:3]:
    print(f"  {line[:100]}...")

# Step 2: Initialize Gemini
print("\n\n🤖 Step 2: Initializing Gemini")
gemini_extractor = get_gemini_extractor()

if not gemini_extractor.initialized:
    print("❌ Gemini not initialized. Check API key.")
    sys.exit(1)

# Step 3: Test FIR
test_fir = """
On 14th September 2025, complainant Rahul Verma reported that he was 
assaulted and his mobile phone was stolen near Narsapur Road by accused 
Ramu Singh. The accused threatened the victim saying "I will kill you" 
and fled towards Market Area.
"""

print("\n\n📄 Step 3: Test FIR")
print(test_fir)

# Step 4: Extract entities
print("\n🔍 Step 4: Extracting Entities")
try:
    entities = gemini_extractor.extract_entities(test_fir)
    print("✓ Entities extracted:")
    print(json.dumps(entities, indent=2))
except Exception as e:
    print(f"❌ Entity extraction failed: {e}")
    sys.exit(1)

# Step 5: Map to legal sections
print("\n\n⚖️  Step 5: Mapping to Legal Sections")
try:
    legal_mapper = create_gemini_legal_mapper(gemini_extractor.model)
    legal_sections = legal_mapper.map_to_legal_sections(test_fir, entities, legal_context)
    
    print(f"\n✓ Matched {len(legal_sections)} legal sections:")
    print("\n" + "=" * 70)
    for i, section in enumerate(legal_sections, 1):
        print(f"\n{i}. {section.get('section_number', 'N/A')}")
        print(f"   Title: {section.get('title', 'N/A')}")
        print(f"   Explanation: {section.get('explanation', 'N/A')}")
    print("\n" + "=" * 70)
    
except Exception as e:
    print(f"❌ Legal mapping failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n\n✅ TEST COMPLETE!")
print("=" * 70)
