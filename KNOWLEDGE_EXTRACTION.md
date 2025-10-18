# Legal Knowledge Extraction Script

## Overview

This script extracts legal sections from PDF and PowerPoint files using **Gemini 2.5 Flash** AI model. It processes all documents in a folder, chunks the text, sends it to Gemini for analysis, and creates a structured JSON knowledge base.

## Features

✅ **Multi-format support**: PDF (.pdf) and PowerPoint (.pptx)  
✅ **Automatic chunking**: Splits large documents into ~1000 token chunks  
✅ **Gemini 2.5 Flash**: Uses latest AI model for extraction  
✅ **Structured output**: JSON format with section_number, title, explanation  
✅ **Debug logging**: Real-time progress indicators  
✅ **Duplicate removal**: Ensures unique legal sections  
✅ **No regex**: Pure AI-based extraction (no fallback)  
✅ **Incremental building**: Appends to existing knowledge base instead of overwriting  

## Setup

### 1. **Ensure dependencies are installed**

```powershell
pip install pypdf python-pptx google-generativeai python-dotenv
```

Or use requirements.txt:
```powershell
pip install -r requirements.txt
```

### 2. **Verify .env file exists**

Ensure `backend/.env` contains:
```
GOOGLE_API_KEY=AIzaSyARcJWEONItPINU_n1-rQM5njUk-Q8KmOk
```

### 3. **Create documents folder**

```powershell
mkdir documents
```

Place your PDF and PPTX files in this folder.

## Usage

### **Basic Usage (default folder)**

```powershell
python backend/extract_legal_knowledge.py
```

This will:
1. Look for files in `documents/` folder
2. Process all .pdf and .pptx files
3. **Append** to existing `knowledge_base/legal_knowledge.json` (or create if doesn't exist)

### **Custom Folder**

```powershell
python backend/extract_legal_knowledge.py "path/to/your/documents"
```

### **Incremental Building Workflow**

The script is designed for **incremental knowledge base building**:

1. **First run**: Process initial documents
   ```powershell
   # Add ipc_sections.pdf to documents/
   python backend/extract_legal_knowledge.py
   # Creates legal_knowledge.json with IPC sections
   ```

2. **Second run**: Add more documents
   ```powershell
   # Add crpc_sections.pdf to documents/
   python backend/extract_legal_knowledge.py
   # Appends CrPC sections to existing knowledge base
   ```

3. **Third run**: Continue building
   ```powershell
   # Add case_laws.pptx to documents/
   python backend/extract_legal_knowledge.py
   # Adds case law sections without losing previous data
   ```

**Benefits:**
- ✅ Never lose existing data
- ✅ Process documents in batches
- ✅ Build knowledge base over time
- ✅ Automatic duplicate prevention

## How It Works

### **1. File Discovery**
- Scans folder for .pdf and .pptx files
- Reports number of files found

### **2. Text Extraction**
- **PDF**: Uses `pypdf` to extract text from all pages
- **PPTX**: Uses `python-pptx` to extract text from all slides

### **3. Text Chunking**
- Splits text into chunks of ~3000 characters (~1000 tokens)
- Ensures chunks don't break mid-sentence

### **4. Gemini Processing**
For each chunk, sends this prompt:

```
You are a legal expert analyzing Indian legal documents. 
Extract all legal sections mentioned in the following text.

Return a JSON array with:
- section_number (e.g., "IPC Section 302")
- title (e.g., "Murder")
- explanation (concise description)
```

### **5. Response Parsing**
- Parses JSON response from Gemini
- Handles markdown code blocks
- Validates structure

### **6. Deduplication & Merging**
- Loads existing `legal_knowledge.json` if it exists
- Compares new sections with existing ones
- Only adds sections that don't already exist (based on section_number)
- Preserves original data for existing sections
- Reports how many new sections were added

### **7. Output**
Saves to `legal_knowledge.json`:

```json
{
  "legal_sections": [
    {
      "section_number": "IPC Section 302",
      "title": "Murder",
      "explanation": "Whoever commits murder shall be punished..."
    }
  ],
  "total_sections": 150,
  "extraction_method": "gemini-2.5-flash",
  "source": "Extracted from PDF and PPTX documents"
}
```

## Debug Output

The script provides detailed progress indicators:

```
======================================================================
LEGAL KNOWLEDGE EXTRACTOR - GEMINI 2.5 FLASH
======================================================================
Documents folder: D:\...\documents
======================================================================

======================================================================
INITIALIZING GEMINI 2.5 FLASH
======================================================================
✓ Loaded .env from: D:\...\backend\.env
✓ API key found: AIzaSyARcJWEONItPI...
✓ Gemini 2.5 Flash initialized successfully (REST API)
======================================================================

======================================================================
SCANNING FOLDER: D:\...\documents
======================================================================
✓ Found 2 PDF files
✓ Found 1 PPTX files
✓ Total files to process: 3

======================================================================
PROCESSING FILE: legal_sections.pdf
======================================================================

📄 Processing PDF: legal_sections.pdf
  ✓ Extracted page 1/50
  ✓ Extracted page 2/50
  ...
✓ PDF extracted: 45000 characters from 50 pages
✓ Text split into 15 chunks (~3000 chars each)

--- Processing Chunk 1/15 ---
🤖 Chunk 1 sent to Gemini...
✓ Response received from Gemini
✓ Extracted 8 legal sections from chunk 1
  Example: IPC Section 302 - Murder

--- Processing Chunk 2/15 ---
🤖 Chunk 2 sent to Gemini...
✓ Response received from Gemini
✓ Extracted 6 legal sections from chunk 2
  Example: IPC Section 304 - Culpable Homicide

...

✓ Finished processing legal_sections.pdf
✓ Total sections extracted: 120

======================================================================
ALL FILES PROCESSED
======================================================================
✓ Total legal sections extracted: 250

======================================================================
SAVING KNOWLEDGE BASE
======================================================================
✓ Found existing knowledge base: legal_knowledge.json
✓ Loaded 100 existing sections
✓ Added 50 new sections
✓ Total unique sections: 150
✓ Saved knowledge base with 150 sections
✓ Output file: D:\...\knowledge_base\legal_knowledge.json
✓ File size: 45.23 KB

📋 Sample sections:

  1. IPC Section 302
     Title: Murder
     Explanation: Whoever commits murder shall be punished with death...

  2. IPC Section 304
     Title: Culpable Homicide Not Amounting to Murder
     Explanation: Whoever commits culpable homicide not amounting...

======================================================================
✓ EXTRACTION COMPLETE!
======================================================================
```

## Output Structure

### **legal_knowledge.json**

```json
{
  "legal_sections": [
    {
      "section_number": "IPC Section 302",
      "title": "Murder",
      "explanation": "Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine."
    },
    {
      "section_number": "IPC Section 304",
      "title": "Culpable Homicide Not Amounting to Murder",
      "explanation": "Whoever commits culpable homicide not amounting to murder shall be punished with imprisonment for life, or imprisonment for a term which may extend to ten years, and shall also be liable to fine."
    }
  ],
  "total_sections": 150,
  "extraction_method": "gemini-2.5-flash",
  "source": "Extracted from PDF and PPTX documents"
}
```

## Error Handling

### **No files found**
```
⚠️  No PDF or PPTX files found in folder
```
**Solution**: Add .pdf or .pptx files to the documents folder

### **API key not found**
```
❌ GOOGLE_API_KEY not found in environment
```
**Solution**: Ensure `backend/.env` exists with valid API key

### **Empty response from Gemini**
```
⚠️  Empty response from Gemini
```
**Solution**: Check API key validity and rate limits

### **JSON parsing error**
```
❌ JSON parsing error for chunk 5: Expecting value: line 1 column 1
```
**Solution**: Gemini occasionally returns malformed JSON. The script continues processing other chunks.

## Performance

- **Processing speed**: ~5-10 seconds per chunk (depends on API latency)
- **Rate limits**: Gemini 2.5 Flash free tier = 15 requests/minute
- **Large documents**: A 50-page PDF with 15 chunks takes ~2-3 minutes

## Cost Estimation

**Gemini 2.5 Flash Pricing:**
- Free tier: 15 requests/minute, 1M tokens/day
- Paid tier: $0.075 per 1M input tokens

**Example:**
- 100-page PDF = ~30 chunks
- 30 chunks × 1000 tokens = 30,000 tokens
- Cost: ~$0.002 (very low)

## Troubleshooting

### **Import errors**
```powershell
pip install pypdf python-pptx google-generativeai python-dotenv
```

### **Permission errors**
Run with administrator privileges or check folder permissions

### **Rate limit exceeded**
Wait 1 minute or upgrade to paid tier

## Integration with Backend

The generated `legal_knowledge.json` can be used by:

1. **`backend/knowledge_loader.py`** - Load legal references
2. **`backend/legal_mapper.py`** - Map FIR text to legal sections
3. **Frontend** - Display legal sections in UI

## Next Steps

1. Place PDF/PPTX files in `documents/` folder
2. Run the extraction script
3. Verify `knowledge_base/legal_knowledge.json` is created
4. Use the knowledge base in your FIR analysis system

---

**Status:** Ready to extract legal knowledge from documents! 📚⚖️
