"""Quick verification of entity extraction fixes"""
import sys
sys.path.insert(0, '.')

from backend.fir_parser import extract_entities

# Test case with comprehensive FIR
test_text = """
On 14th September 2025, complainant Rahul Verma, S/o Ramesh Verma, reported that he was 
assaulted and his mobile phone was stolen near Narsapur Road by accused Ramu Singh and 
Shyam Kumar. The incident took place at around 3 PM. Witness Mr. Prakash Sharma was present. 
The accused threatened the victim saying "I will kill you and burn your house" and fled 
towards Market Area. Contact: 9876543210.
"""

print("Testing entity extraction...")
print("=" * 60)

entities = extract_entities(test_text)

print(f"\n✓ Names ({len(entities['names'])}): {entities['names']}")
print(f"✓ Dates ({len(entities['dates'])}): {entities['dates']}")
print(f"✓ Locations ({len(entities['locations'])}): {entities['locations']}")
print(f"✓ Phones ({len(entities['phone_numbers'])}): {entities['phone_numbers']}")
print(f"✓ Crimes ({len(entities['crimes'])}): {entities['crimes']}")
print(f"✓ Threats ({len(entities['threats'])}): {entities['threats']}")
print(f"✓ Objects ({len(entities['objects'])}): {entities['objects']}")

print("\n" + "=" * 60)
print("Expected:")
print("Names: Rahul Verma, Ramesh Verma, Ramu Singh, Shyam Kumar, Prakash Sharma")
print("Dates: 14th September 2025")
print("Locations: Narsapur Road, Market Area")
print("Crimes: assault, theft")
print("Threats: threaten, kill, burn")
