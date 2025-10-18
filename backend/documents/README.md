# Documents Folder

Place your PDF and PowerPoint files here for legal knowledge extraction.

## Supported Formats

- **PDF**: `.pdf` files
- **PowerPoint**: `.pptx` files

## Usage

1. Copy your legal document files to this folder
2. Run the extraction script:
   ```powershell
   python backend/extract_legal_knowledge.py
   ```
3. The script will process all files and create `knowledge_base/legal_knowledge.json`

## Example Files

You can add files like:
- `ipc_sections.pdf` - Indian Penal Code sections
- `crpc_sections.pdf` - Criminal Procedure Code sections
- `legal_reference.pptx` - PowerPoint with legal information
- `case_laws.pdf` - Case law references

## Notes

- Files can be any size (script automatically chunks large documents)
- Multiple files will be processed sequentially
- Duplicate legal sections are automatically removed
- Progress is shown in real-time during extraction
