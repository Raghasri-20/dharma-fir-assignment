"""Test Gemini integration"""
import sys
sys.path.insert(0, '.')

from backend.gemini_extractor import get_gemini_extractor

print("=" * 70)
print("TESTING GEMINI AI INTEGRATION")
print("=" * 70)

# Get extractor
extractor = get_gemini_extractor()

print(f"\n✓ Gemini Initialized: {extractor.initialized}")

if not extractor.initialized:
    print("\n❌ Gemini not initialized. Check:")
    print("   1. backend/.env file exists")
    print("   2. GOOGLE_API_KEY is set in .env")
    print("   3. google-generativeai is installed")
    sys.exit(1)

# Test case
test_text = "He threatened to kill Ramu and burn his hut."

print(f"\n📤 Testing with: {test_text}")

try:
    entities = extractor.extract_entities(test_text)
    
    print("\n✅ Extraction successful!")
    print(f"\n📋 ENTITIES:")
    print(f"   Names: {entities.get('names', [])}")
    print(f"   Dates: {entities.get('dates', [])}")
    print(f"   Locations: {entities.get('locations', [])}")
    print(f"   Phones: {entities.get('phone_numbers', [])}")
    print(f"   Crimes: {entities.get('crimes', [])}")
    print(f"   Threats: {entities.get('threats', [])}")
    print(f"   Objects: {entities.get('objects', [])}")
    
except Exception as e:
    print(f"\n❌ Extraction failed: {e}")
    sys.exit(1)

print(f"\n{'=' * 70}")
print("✓ Test complete!")
