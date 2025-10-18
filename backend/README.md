# Backend - Dharma FIR Assistant

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
