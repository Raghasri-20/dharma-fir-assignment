"""
Script to reorganize project structure
Moves all files into frontend/ and backend/ folders
"""
import os
import shutil
from pathlib import Path

# Get project root
project_root = Path(__file__).parent
print(f"Project root: {project_root}")

# Define new structure
moves = [
    # Move knowledge_base to backend
    ("knowledge_base", "backend/knowledge_base"),
    
    # Move documents to backend
    ("documents", "backend/documents"),
    
    # Move writeup to backend
    ("writeup", "backend/writeup"),
    
    # Move test scripts to backend
    ("test_extraction.py", "backend/test_extraction.py"),
    ("test_legal_mapping.py", "backend/test_legal_mapping.py"),
    
    # Move documentation files to backend
    ("KNOWLEDGE_EXTRACTION.md", "backend/docs/KNOWLEDGE_EXTRACTION.md"),
    ("INCREMENTAL_BUILDING.md", "backend/docs/INCREMENTAL_BUILDING.md"),
    ("GEMINI_LEGAL_MAPPING.md", "backend/docs/GEMINI_LEGAL_MAPPING.md"),
    ("LEGAL_MAPPING_SUMMARY.md", "backend/docs/LEGAL_MAPPING_SUMMARY.md"),
    ("TIMEOUT_FIX.md", "backend/docs/TIMEOUT_FIX.md"),
    ("EXTRACTION_SUMMARY.md", "backend/docs/EXTRACTION_SUMMARY.md"),
]

print("\n" + "="*70)
print("REORGANIZING PROJECT STRUCTURE")
print("="*70)

for source, destination in moves:
    source_path = project_root / source
    dest_path = project_root / destination
    
    if source_path.exists():
        print(f"\n📦 Moving: {source}")
        print(f"   → {destination}")
        
        # Create destination directory if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file or directory
        try:
            if source_path.is_dir():
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                shutil.move(str(source_path), str(dest_path))
            else:
                shutil.move(str(source_path), str(dest_path))
            print(f"   ✓ Moved successfully")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print(f"\n⚠️  Not found: {source}")

print("\n" + "="*70)
print("CREATING README FILES")
print("="*70)

# Create backend README
backend_readme = """# Backend - Dharma FIR Assistant

## Structure

```
backend/
├── __pycache__/
├── docs/                    # Documentation
├── documents/               # Source PDFs/PPTs for knowledge extraction
├── knowledge_base/          # Extracted legal knowledge (JSON)
├── writeup/                 # Approach notes and writeup
├── .env                     # Environment variables (API key)
├── extract_legal_knowledge.py
├── fir_parser.py
├── gemini_extractor.py
├── gemini_legal_mapper.py
├── knowledge_loader.py
├── legal_mapper.py
├── main.py                  # FastAPI application
├── summarizer.py
├── test_extraction.py
└── test_legal_mapping.py
```

## Running Backend

```powershell
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

## Documentation

See `docs/` folder for detailed documentation:
- `KNOWLEDGE_EXTRACTION.md` - How to extract legal sections from PDFs
- `GEMINI_LEGAL_MAPPING.md` - Legal section mapping approach
- `TIMEOUT_FIX.md` - Performance optimizations
"""

backend_readme_path = project_root / "backend" / "README.md"
with open(backend_readme_path, 'w', encoding='utf-8') as f:
    f.write(backend_readme)
print(f"✓ Created: backend/README.md")

# Create frontend README
frontend_readme = """# Frontend - Dharma FIR Assistant

## Structure

```
frontend/
├── public/
├── src/
│   ├── App.jsx              # Main application
│   ├── FIRForm.jsx          # FIR input form
│   ├── FIRResult.jsx        # Results display
│   ├── LegalSectionCard.jsx # Legal section cards
│   ├── api.js               # API client
│   ├── styles.css           # Global styles
│   └── main.jsx             # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Running Frontend

```powershell
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build
```

## Features

- Real-time FIR analysis
- Entity extraction display
- Collapsible legal section cards
- Loading states and error handling
- Responsive design
"""

frontend_readme_path = project_root / "frontend" / "README.md"
with open(frontend_readme_path, 'w', encoding='utf-8') as f:
    f.write(frontend_readme)
print(f"✓ Created: frontend/README.md")

print("\n" + "="*70)
print("✓ REORGANIZATION COMPLETE!")
print("="*70)

print("\n📁 New Project Structure:")
print("""
dharma-fir-assignment/
├── backend/
│   ├── docs/                    # All documentation
│   ├── documents/               # Source PDFs/PPTs
│   ├── knowledge_base/          # Legal knowledge JSON
│   ├── writeup/                 # Approach notes
│   ├── *.py                     # Python modules
│   └── README.md
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── README.md
├── README.md                    # Main project README
└── INSTALL.md                   # Installation guide
""")

print("\n⚠️  Don't forget to update:")
print("  1. Import paths in Python files (if needed)")
print("  2. File paths in documentation")
print("  3. .gitignore if necessary")
