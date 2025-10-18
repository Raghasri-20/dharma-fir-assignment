# Complete Setup Guide - Dharma FIR Assistant

## 🎯 Project Overview

AI-powered FIR (First Information Report) analysis system using **Gemini 2.5 Flash** for entity extraction and legal section mapping.

---

## 🚀 Quick Start

### **Backend Setup**

1. **Navigate to project root:**
   ```powershell
   cd "D:\Random Reverse Engineering Projects\dharma-fir-assignmnet\dharma-fir-assignment"
   ```

2. **Activate virtual environment:**
   ```powershell
   .\newenv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Verify Gemini setup:**
   ```powershell
   python test_gemini.py
   ```
   
   Expected output:
   ```
   ✓ Gemini Initialized: True
   ✅ Extraction successful!
   ```

5. **Start backend server:**
   ```powershell
   uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
   ```
   
   Should see:
   ```
   INFO: Gemini AI initialized successfully with gemini-2.5-flash (REST)
   INFO: Uvicorn running on http://127.0.0.1:8000
   ```

### **Frontend Setup**

1. **Open new terminal and navigate to frontend:**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Start development server:**
   ```powershell
   npm run dev
   ```
   
   Should see:
   ```
   VITE ready in xxx ms
   ➜  Local:   http://localhost:5173/
   ```

4. **Open in browser:**
   - http://localhost:5173

---

## 📁 Project Structure

```
dharma-fir-assignment/
├── backend/
│   ├── .env                    # API key configuration
│   ├── main.py                 # FastAPI app with Gemini integration
│   ├── gemini_extractor.py     # Gemini AI entity extraction
│   ├── fir_parser.py           # FIR parsing logic
│   ├── legal_mapper.py         # Legal section mapping
│   ├── summarizer.py           # Summary generation
│   └── knowledge_loader.py     # Legal reference loader
├── frontend/
│   └── src/
│       ├── App.jsx             # Main app component
│       ├── FIRForm.jsx         # Input form
│       ├── FIRResult.jsx       # Results display
│       ├── LoadingSpinner.jsx  # Loading animation
│       ├── ErrorMessage.jsx    # Error handling
│       ├── LegalSectionCard.jsx # Collapsible cards
│       ├── HighlightedText.jsx # Entity highlighting
│       └── styles.css          # Complete styling
├── requirements.txt            # Python dependencies
├── test_gemini.py             # Gemini integration test
└── COMPLETE_SETUP.md          # This file
```

---

## 🔑 Configuration

### **Backend (.env file)**

Location: `backend/.env`

```
GOOGLE_API_KEY=AIzaSyARcJWEONItPINU_n1-rQM5njUk-Q8KmOk
```

### **API Endpoints**

- **Health Check**: `GET http://127.0.0.1:8000/`
- **Process FIR**: `POST http://127.0.0.1:8000/process`
- **Parse FIR**: `POST http://127.0.0.1:8000/parse-fir`
- **API Docs**: `http://127.0.0.1:8000/docs`

---

## ✨ Features

### **Backend**
- ✅ Gemini 2.5 Flash AI integration
- ✅ REST API (not gRPC/Vertex AI)
- ✅ Entity extraction: names, dates, locations, crimes, threats, objects
- ✅ Legal section mapping
- ✅ Summary generation
- ✅ Error handling with friendly messages
- ✅ No regex fallback (Gemini only)

### **Frontend**
- ✅ Loading animation with progress steps
- ✅ Color-coded entity highlighting
- ✅ Interactive hover tooltips
- ✅ Collapsible legal section cards
- ✅ Copy/Export functionality (Summary, JSON, Download)
- ✅ Error messages with retry button
- ✅ Responsive design
- ✅ Modern gradient UI
- ✅ Accessibility features

---

## 🧪 Testing

### **Test Gemini Integration**
```powershell
python test_gemini.py
```

### **Test API Endpoint**
```powershell
curl -X POST http://127.0.0.1:8000/parse-fir `
  -H "Content-Type: application/json" `
  -d '{\"text\": \"He threatened to kill Ramu and burn his hut.\"}'
```

### **Expected Response**
```json
{
  "entities": {
    "names": ["Ramu"],
    "dates": [],
    "locations": [],
    "phone_numbers": [],
    "crimes": ["criminal intimidation"],
    "threats": ["kill", "burn"],
    "objects": ["hut"]
  },
  "legal_sections": [...],
  "summary": "...",
  "extraction_method": "gemini"
}
```

---

## 🐛 Troubleshooting

### **Issue: "404 models/gemini-pro not found"**
**Solution:** Model name updated to `models/gemini-2.5-flash`
- Check `backend/gemini_extractor.py` line 44

### **Issue: "ALTS creds ignored. Not running on GCP"**
**Solution:** This is a warning, not an error. Gemini is using REST API correctly.

### **Issue: "Pydantic version mismatch"**
**Solution:**
```powershell
pip install --upgrade pydantic pydantic-core
pip install -r requirements.txt
```

### **Issue: "GOOGLE_API_KEY not found"**
**Solution:** Ensure `backend/.env` exists with the API key

### **Issue: Frontend can't connect to backend**
**Solution:** 
1. Verify backend is running on port 8000
2. Check CORS settings in `backend/main.py`
3. Ensure frontend is using correct API URL in `src/api.js`

---

## 📊 Dependencies

### **Backend (Python)**
```
fastapi==0.115.2
uvicorn[standard]==0.30.6
pydantic>=2.9.2
python-multipart==0.0.12
httpx==0.27.2
google-generativeai
python-dotenv==1.0.1
```

### **Frontend (Node.js)**
```json
{
  "axios": "^1.7.7",
  "react": "^18.3.1",
  "react-dom": "^18.3.1"
}
```

---

## 🎨 UI Preview

### **Loading State**
- Animated spinner
- "Analyzing FIR with Gemini..." message
- Progress steps with checkmarks

### **Results Display**
- Gradient header with export buttons
- Summary card with border accent
- Entity cards in responsive grid
- Color-coded entity tags
- Highlighted FIR text with legend
- Collapsible legal section cards

### **Error State**
- Warning icon
- Friendly error message
- Helpful suggestions
- Retry button

---

## 📝 Sample FIR Text

```
On 14th September 2025, complainant Rahul Verma, S/o Ramesh Verma, 
reported that he was assaulted and his mobile phone was stolen near 
Narsapur Road by accused Ramu Singh and Shyam Kumar. The incident 
took place at around 3 PM. Witness Mr. Prakash Sharma was present. 
The accused threatened the victim saying "I will kill you and burn 
your house" and fled towards Market Area. Contact: 9876543210.
```

---

## 🔐 Security Notes

- API key stored in `.env` file (not committed to git)
- Add `backend/.env` to `.gitignore` in production
- Use environment variables in deployment
- CORS configured for local development only

---

## 🚀 Deployment

### **Backend (Production)**
1. Set environment variable: `GOOGLE_API_KEY`
2. Update CORS origins in `backend/main.py`
3. Use production ASGI server (Gunicorn + Uvicorn)
4. Deploy to cloud platform (Heroku, AWS, GCP, etc.)

### **Frontend (Production)**
1. Update API URL in `src/api.js`
2. Build: `npm run build`
3. Deploy `dist/` folder to hosting (Netlify, Vercel, etc.)

---

## 📚 Documentation

- **Backend API**: http://127.0.0.1:8000/docs (Swagger UI)
- **Frontend Features**: `frontend/FRONTEND_FEATURES.md`
- **Gemini Setup**: `INSTALL.md`

---

## ✅ Checklist

- [x] Gemini 2.5 Flash integration
- [x] REST API (not gRPC)
- [x] Entity extraction working
- [x] Loading animation
- [x] Entity highlighting
- [x] Collapsible legal cards
- [x] Error handling with retry
- [x] Copy/Export features
- [x] Responsive design
- [x] Accessibility features

---

## 🎉 Success Criteria

✅ Backend starts without errors  
✅ `test_gemini.py` passes  
✅ Frontend loads at http://localhost:5173  
✅ Can submit FIR text and see results  
✅ Entities are highlighted in different colors  
✅ Legal sections are collapsible  
✅ Can copy/download results  
✅ Error messages appear when Gemini fails  

---

**Status:** ✅ Complete and ready for use!
