# Testing the FIR Parser

## Quick Test

Run the test script to verify all functionality:

```powershell
python test_parser.py
```

## Expected Output

### Test Case 1: Comprehensive FIR
Should extract:
- **Names**: Rahul Verma, Ramesh Verma, Ramu Singh, Shyam Kumar, Prakash Sharma
- **Dates**: 14th September 2025
- **Locations**: Narsapur Road, Market Area
- **Phone**: 9876543210
- **Crimes**: assault, theft
- **Threats**: threaten, kill, burn
- **Objects**: mobile, phone

### Test Case 2: Only Threats
Should extract:
- **Threats**: threaten, kill, burn
- **Legal Sections**: IPC 506, BNS 351

## Testing via API

1. **Start backend**:
```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

2. **Test with curl**:
```powershell
curl -X POST http://127.0.0.1:8000/parse-fir `
  -H "Content-Type: application/json" `
  -d '{\"text\": \"On 14th September 2025, complainant Rahul Verma reported that he was assaulted and his mobile was stolen near Narsapur Road by accused Ramu Singh. The accused threatened to kill the victim.\"}'
```

3. **Or use the frontend**:
```powershell
cd frontend
npm run dev
```
Open http://127.0.0.1:5173 and paste FIR text.

## Sample FIR Texts

### Example 1: Theft + Assault + Threats
```
On 14th September 2025, complainant Rahul Verma, S/o Ramesh Verma, reported that he was 
assaulted and his mobile phone was stolen near Narsapur Road by accused Ramu Singh and 
Shyam Kumar. The incident took place at around 3 PM. Witness Mr. Prakash Sharma was present. 
The accused threatened the victim saying "I will kill you and burn your house" and fled 
towards Market Area. Contact: 9876543210.
```

**Expected**:
- Crimes: assault, theft
- Threats: threaten, kill, burn
- Sections: IPC 506, BNS 351, IPC 323, IPC 379

### Example 2: Only Threats
```
The accused threatened to kill and burn the victim.
```

**Expected**:
- Threats: threaten, kill, burn
- Sections: IPC 506, BNS 351

### Example 3: Cheating Case
```
On 12/09/2024, complainant Suresh Kumar reported that he was cheated of Rs. 50,000 by 
unknown persons posing as bank officials in Connaught Place, New Delhi. The accused called 
from 9876543210 and obtained OTP to siphon funds.
```

**Expected**:
- Crimes: cheating
- Objects: rs, phone
- Sections: IPC 420, IT Act 66C

## Troubleshooting

### Empty entities
- Check that your FIR text has proper capitalization (e.g., "Rahul Verma" not "rahul verma")
- Ensure keywords like "complainant", "accused", "witness" are present
- Dates should be in format: `14th September 2025` or `12/09/2024`
- Locations should follow prepositions: `near Narsapur Road`, `at Market Area`

### Names not extracted
- Names must be capitalized: `Rahul Verma` ✅, `rahul verma` ❌
- Must follow keywords: `complainant Rahul Verma`, `accused Ramu Singh`
- Or use titles: `Mr. Prakash Sharma`
- Or relationships: `S/o Ramesh Verma`

### Threats not detected
- Use keywords: `threaten`, `kill`, `burn`, `harm`, `intimidate`, `extort`
- Example: "The accused threatened to kill the victim"
