# Dharma FIR Assistant

AI-powered FIR (First Information Report) analysis system using **Gemini 2.5 Flash** for entity extraction and legal section mapping.

## 🎯 Features

- ✅ **Entity Extraction**: Extracts names, dates, locations, crimes, threats, objects, vehicles
- ✅ **Legal Section Mapping**: Maps FIR to relevant IPC/CrPC sections using AI
- ✅ **Knowledge Base**: Dynamically built from PDFs and PowerPoint files
- ✅ **Two-Stage Processing**: Initial extraction + refinement for accuracy
- ✅ **Modern UI**: React frontend with collapsible cards and real-time feedback

## 📁 Project Structure

```
dharma-fir-assignment/
├── backend/                     # FastAPI backend
│   ├── docs/                    # Documentation (KNOWLEDGE_EXTRACTION.md, etc.)
│   ├── documents/               # Source PDFs/PPTs for knowledge extraction
│   ├── knowledge_base/          # Extracted legal knowledge (JSON)
│   ├── writeup/                 # Approach notes and technical writeup
│   ├── main.py                  # FastAPI application
│   ├── gemini_extractor.py      # Entity extraction using Gemini
│   ├── gemini_legal_mapper.py   # Legal section mapping using Gemini
│   ├── knowledge_loader.py      # Knowledge base loader
│   ├── extract_legal_knowledge.py  # PDF/PPT extraction script
│   ├── test_extraction.py       # Test scripts
│   ├── .env                     # API key (GOOGLE_API_KEY)
│   └── README.md
├── frontend/                    # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx              # Main application
│   │   ├── FIRForm.jsx          # FIR input form
│   │   ├── FIRResult.jsx        # Results display
│   │   ├── LegalSectionCard.jsx # Legal section cards
│   │   ├── api.js               # API client
│   │   └── styles.css           # Styling
│   ├── package.json
│   └── README.md
├── README.md                    # This file
├── INSTALL.md                   # Installation guide
└── requirements.txt             # Python dependencies
```

## Prerequisites

- Python 3.10+
- Node.js 18+

## Backend Setup (FastAPI)

```bash
python -m venv .venv
. .venv/Scripts/activate  # On Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

FastAPI docs: http://127.0.0.1:8000/docs

## Frontend Setup (Vite + React)

```bash
cd frontend
npm install
npm run dev
```

Vite dev server: http://127.0.0.1:5173

## API Contract

- POST `/process`
  - Request: `{ "text": string }`
  - Response: `{ entities, legal_sections, summary, references }`

## 🚀 Quick Start

### 1. Run Reorganization Script
```powershell
python reorganize_structure.py
```

This will move all files into `backend/` and `frontend/` folders.

### 2. Start Backend
```powershell
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Start Frontend
```powershell
cd frontend
npm run dev
```

### 4. Open Browser
Navigate to http://localhost:5173

## 📚 Documentation

All documentation is in `backend/docs/`:
- `KNOWLEDGE_EXTRACTION.md` - How to extract legal sections from PDFs
- `GEMINI_LEGAL_MAPPING.md` - Legal section mapping approach
- `TIMEOUT_FIX.md` - Performance optimizations
- `INCREMENTAL_BUILDING.md` - Building knowledge base incrementally

Technical writeup: `backend/writeup/dharma_approach_note.md`

## 🔑 API Key

Create `backend/.env`:
```
GOOGLE_API_KEY=your_api_key_here
```

## 🎯 Key Technologies

- **AI Model**: Gemini 2.5 Flash
- **Backend**: FastAPI, Python 3.10+
- **Frontend**: React 18, Vite
- **Document Processing**: pypdf, python-pptx
- **API**: Google Generative AI SDK
