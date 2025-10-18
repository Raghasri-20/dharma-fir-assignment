# Incremental Knowledge Base Building Guide

## Overview

The extraction script **appends** to your existing knowledge base instead of overwriting it. This allows you to build your legal knowledge base incrementally over time.

## How It Works

### **Merge Logic**

1. **Check for existing file**: Looks for `legal_knowledge.json`
2. **Load existing sections**: Reads all previously extracted sections
3. **Process new documents**: Extracts sections from current batch
4. **Merge**: Adds only NEW sections (based on `section_number`)
5. **Preserve**: Keeps original data for existing sections
6. **Save**: Writes combined knowledge base

### **Duplicate Prevention**

- Sections are identified by `section_number` (e.g., "IPC Section 302")
- If a section already exists, the **original is preserved**
- New extraction is skipped for that section
- This prevents data loss and maintains consistency

## Workflow Examples

### **Example 1: Building from Scratch**

**Day 1**: Extract IPC sections
```powershell
# Add ipc_sections.pdf to documents/
python backend/extract_legal_knowledge.py
```
**Output:**
```
✓ Creating new knowledge base: legal_knowledge.json
✓ Added 120 new sections
✓ Total unique sections: 120
```

**Day 2**: Add CrPC sections
```powershell
# Add crpc_sections.pdf to documents/
python backend/extract_legal_knowledge.py
```
**Output:**
```
✓ Found existing knowledge base: legal_knowledge.json
✓ Loaded 120 existing sections
✓ Added 85 new sections
✓ Total unique sections: 205
```

**Day 3**: Add case laws
```powershell
# Add case_laws.pptx to documents/
python backend/extract_legal_knowledge.py
```
**Output:**
```
✓ Found existing knowledge base: legal_knowledge.json
✓ Loaded 205 existing sections
✓ Added 45 new sections
✓ Total unique sections: 250
```

### **Example 2: Processing Multiple Sources**

**Batch 1**: Legal textbooks
```powershell
# Add legal_textbook_1.pdf, legal_textbook_2.pdf
python backend/extract_legal_knowledge.py
# Result: 150 sections
```

**Batch 2**: Court judgments
```powershell
# Add judgments_2024.pdf
python backend/extract_legal_knowledge.py
# Result: 150 + 30 = 180 sections
```

**Batch 3**: Legal presentations
```powershell
# Add legal_seminar.pptx, workshop.pptx
python backend/extract_legal_knowledge.py
# Result: 180 + 25 = 205 sections
```

### **Example 3: Re-running Same Files**

If you accidentally run the script twice on the same files:

**First run:**
```
✓ Added 100 new sections
✓ Total unique sections: 100
```

**Second run (same files):**
```
✓ Found existing knowledge base: legal_knowledge.json
✓ Loaded 100 existing sections
✓ Added 0 new sections (all duplicates)
✓ Total unique sections: 100
```

**Result**: No data loss, no duplicates! ✅

## Best Practices

### **1. Organize Documents by Category**

```
documents/
├── ipc_sections.pdf
├── crpc_sections.pdf
├── evidence_act.pdf
└── case_laws/
    ├── 2024_judgments.pdf
    └── landmark_cases.pptx
```

Process each category separately:
```powershell
# Process main documents
python backend/extract_legal_knowledge.py

# Process case laws
python backend/extract_legal_knowledge.py "documents/case_laws"
```

### **2. Keep Source Files**

Don't delete processed PDFs/PPTs. You might want to:
- Re-extract with improved prompts
- Verify extracted data
- Add to documentation

### **3. Backup Knowledge Base**

Before major updates:
```powershell
# Backup current knowledge base
cp knowledge_base/legal_knowledge.json knowledge_base/legal_knowledge_backup.json

# Run extraction
python backend/extract_legal_knowledge.py
```

### **4. Monitor Growth**

Track your knowledge base growth:
```powershell
# Check current size
python -c "import json; data = json.load(open('knowledge_base/legal_knowledge.json')); print(f'Total sections: {data[\"total_sections\"]}')"
```

### **5. Version Control**

Commit knowledge base to git after major updates:
```powershell
git add knowledge_base/legal_knowledge.json
git commit -m "Added 50 new legal sections from CrPC document"
```

## Troubleshooting

### **Issue: "No new sections added"**

**Cause**: All sections already exist in knowledge base

**Solution**: 
- Add different documents to `documents/` folder
- Or manually edit/delete sections you want to re-extract

### **Issue: "Want to replace existing section"**

**Cause**: Existing section has outdated information

**Solution**:
1. Open `knowledge_base/legal_knowledge.json`
2. Find and delete the specific section
3. Re-run extraction script

Example:
```json
{
  "legal_sections": [
    // Delete this section to re-extract
    {
      "section_number": "IPC Section 302",
      "title": "Murder",
      "explanation": "Old explanation..."
    }
  ]
}
```

### **Issue: "Want to start fresh"**

**Solution**:
```powershell
# Backup existing
mv knowledge_base/legal_knowledge.json knowledge_base/legal_knowledge_old.json

# Run extraction (creates new file)
python backend/extract_legal_knowledge.py
```

## Advanced Usage

### **Merge Multiple Knowledge Bases**

If you have multiple `legal_knowledge.json` files:

```python
import json

# Load all files
kb1 = json.load(open('kb1.json'))
kb2 = json.load(open('kb2.json'))

# Merge sections
all_sections = {}
for section in kb1['legal_sections'] + kb2['legal_sections']:
    section_num = section['section_number']
    if section_num not in all_sections:
        all_sections[section_num] = section

# Save merged
merged = {
    "legal_sections": list(all_sections.values()),
    "total_sections": len(all_sections),
    "extraction_method": "gemini-2.5-flash",
    "source": "Merged from multiple sources"
}

json.dump(merged, open('merged_knowledge.json', 'w'), indent=2)
```

### **Filter by Section Type**

Extract only specific types:

```python
import json

kb = json.load(open('knowledge_base/legal_knowledge.json'))

# Filter IPC sections only
ipc_sections = [s for s in kb['legal_sections'] 
                if 'IPC' in s['section_number']]

print(f"Found {len(ipc_sections)} IPC sections")
```

## Summary

✅ **Incremental**: Build knowledge base over time  
✅ **Safe**: Never overwrites existing data  
✅ **Smart**: Automatic duplicate prevention  
✅ **Flexible**: Process documents in any order  
✅ **Reliable**: Preserves original section data  

---

**Start building your legal knowledge base incrementally today!** 📚⚖️
