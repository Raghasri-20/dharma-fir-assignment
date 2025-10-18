# Project Reorganization Instructions

## Current Structure (Before)
```
dharma-fir-assignment/
├── backend/
├── frontend/
├── knowledge_base/          ← To be moved
├── documents/               ← To be moved
├── writeup/                 ← To be moved
├── test_extraction.py       ← To be moved
├── test_legal_mapping.py    ← To be moved
├── *.md files               ← To be moved
├── README.md                ← Stays
├── INSTALL.md               ← Stays
└── requirements.txt         ← Stays
```

## Target Structure (After)
```
dharma-fir-assignment/
├── backend/
│   ├── docs/                # All documentation
│   ├── documents/           # Source PDFs/PPTs
│   ├── knowledge_base/      # Legal knowledge JSON
│   ├── writeup/             # Approach notes
│   ├── *.py files
│   └── README.md
├── frontend/
│   ├── src/
│   ├── package.json
│   └── README.md
├── README.md                # Main project README
├── INSTALL.md               # Installation guide
└── requirements.txt         # Python dependencies
```

## How to Reorganize

### Option 1: Automatic (Recommended)

Run the reorganization script:
```powershell
python reorganize_structure.py
```

This will:
1. Move `knowledge_base/` → `backend/knowledge_base/`
2. Move `documents/` → `backend/documents/`
3. Move `writeup/` → `backend/writeup/`
4. Move test scripts → `backend/`
5. Move documentation files → `backend/docs/`
6. Create README files in backend/ and frontend/

### Option 2: Manual

If you prefer manual reorganization:

1. **Create directories:**
   ```powershell
   mkdir backend\docs
   ```

2. **Move folders:**
   ```powershell
   move knowledge_base backend\knowledge_base
   move documents backend\documents
   move writeup backend\writeup
   ```

3. **Move test files:**
   ```powershell
   move test_extraction.py backend\
   move test_legal_mapping.py backend\
   ```

4. **Move documentation:**
   ```powershell
   move KNOWLEDGE_EXTRACTION.md backend\docs\
   move INCREMENTAL_BUILDING.md backend\docs\
   move GEMINI_LEGAL_MAPPING.md backend\docs\
   move LEGAL_MAPPING_SUMMARY.md backend\docs\
   move TIMEOUT_FIX.md backend\docs\
   move EXTRACTION_SUMMARY.md backend\docs\
   ```

## After Reorganization

### Update Import Paths

If you moved files, update these imports in backend Python files:

**In `backend/main.py`:**
```python
# No changes needed - relative imports work
from .knowledge_loader import load_legal_knowledge
```

**In `backend/knowledge_loader.py`:**
```python
# Update path to knowledge base
KB_PATH = BASE_DIR / "knowledge_base" / "legal_knowledge.json"
```

**In `backend/extract_legal_knowledge.py`:**
```python
# Update output path
output_path = Path(__file__).parent / "knowledge_base" / "legal_knowledge.json"
```

### Test the Setup

1. **Test backend:**
   ```powershell
   cd backend
   uvicorn main:app --reload
   ```

2. **Test frontend:**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Verify knowledge base:**
   ```powershell
   cd backend
   python test_legal_mapping.py
   ```

## Verification Checklist

After reorganization, verify:

- [ ] `backend/knowledge_base/legal_knowledge.json` exists
- [ ] `backend/documents/` contains your PDFs/PPTs
- [ ] `backend/writeup/dharma_approach_note.md` exists
- [ ] `backend/docs/` contains all documentation
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] API calls work (test with frontend)

## Rollback (If Needed)

If something goes wrong, you can manually move files back:
```powershell
move backend\knowledge_base knowledge_base
move backend\documents documents
move backend\writeup writeup
```

## Final Structure

After successful reorganization, you should have:
- ✅ Only 2 main folders: `backend/` and `frontend/`
- ✅ All documentation in `backend/docs/`
- ✅ All source files organized logically
- ✅ README files in each folder
- ✅ Clean project root with only README, INSTALL, requirements.txt

---

**Ready to reorganize?** Run: `python reorganize_structure.py`
