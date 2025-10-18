"""
Extract legal sections from PDFs and PPTs using Gemini 2.5 Flash
Processes all documents in a folder and creates legal_knowledge.json
"""
import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

# PDF and PPT extraction libraries
try:
    from pypdf import PdfReader
    print("✓ pypdf imported successfully")
except ImportError:
    print("❌ pypdf not found. Install with: pip install pypdf")
    sys.exit(1)

try:
    from pptx import Presentation
    print("✓ python-pptx imported successfully")
except ImportError:
    print("❌ python-pptx not found. Install with: pip install python-pptx")
    sys.exit(1)


class LegalKnowledgeExtractor:
    """Extract legal knowledge from documents using Gemini"""
    
    def __init__(self, documents_folder: str):
        self.documents_folder = Path(documents_folder)
        self.model = None
        self.all_sections = []
        
        # Load environment and configure Gemini
        print("\n" + "=" * 70)
        print("INITIALIZING GEMINI 2.5 FLASH")
        print("=" * 70)
        
        # Load API key from backend/.env
        backend_dir = Path(__file__).parent
        env_path = backend_dir / ".env"
        
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            print(f"✓ Loaded .env from: {env_path}")
        else:
            load_dotenv()
            print("✓ Loaded .env from default location")
        
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment")
            sys.exit(1)
        
        print(f"✓ API key found: {api_key[:20]}...")
        
        # Configure Gemini with REST transport
        genai.configure(
            api_key=api_key,
            transport="rest"
        )
        
        # Initialize Gemini 2.5 Flash model
        self.model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        print("✓ Gemini 2.5 Flash initialized successfully (REST API)")
        print("=" * 70 + "\n")
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF file"""
        print(f"\n📄 Processing PDF: {pdf_path.name}")
        
        try:
            reader = PdfReader(str(pdf_path))
            text = ""
            
            for i, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text += page_text + "\n"
                print(f"  ✓ Extracted page {i}/{len(reader.pages)}")
            
            print(f"✓ PDF extracted: {len(text)} characters from {len(reader.pages)} pages")
            return text.strip()
            
        except Exception as e:
            print(f"❌ Error extracting PDF {pdf_path.name}: {e}")
            return ""
    
    def extract_text_from_pptx(self, pptx_path: Path) -> str:
        """Extract text from PowerPoint file"""
        print(f"\n📊 Processing PPTX: {pptx_path.name}")
        
        try:
            prs = Presentation(str(pptx_path))
            text = ""
            
            for i, slide in enumerate(prs.slides, 1):
                slide_text = []
                
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        slide_text.append(shape.text)
                
                text += "\n".join(slide_text) + "\n\n"
                print(f"  ✓ Extracted slide {i}/{len(prs.slides)}")
            
            print(f"✓ PPTX extracted: {len(text)} characters from {len(prs.slides)} slides")
            return text.strip()
            
        except Exception as e:
            print(f"❌ Error extracting PPTX {pptx_path.name}: {e}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 3000) -> List[str]:
        """
        Split text into chunks of approximately chunk_size characters
        (roughly 1000 tokens = ~3000-4000 characters)
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        print(f"✓ Text split into {len(chunks)} chunks (~{chunk_size} chars each)")
        return chunks
    
    def extract_legal_sections_from_chunk(self, chunk: str, chunk_num: int) -> List[Dict[str, str]]:
        """Extract legal sections from a text chunk using Gemini"""
        print(f"\n🤖 Chunk {chunk_num} sent to Gemini...")
        
        prompt = f"""You are a legal expert analyzing Indian legal documents. Extract all legal sections mentioned in the following text.

Text:
{chunk}

Return a JSON array of legal sections with the following structure:
[
  {{
    "section_number": "IPC Section 302",
    "title": "Murder",
    "explanation": "Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine."
  }}
]

Rules:
1. Extract ALL legal sections mentioned (IPC, CrPC, etc.)
2. Include the full section number (e.g., "IPC Section 302", "CrPC Section 154")
3. Provide a clear title for each section
4. Give a concise explanation of what the section covers
5. Return ONLY the JSON array, no additional text
6. If no legal sections are found, return an empty array: []

Return the JSON array now:"""

        try:
            response = self.model.generate_content([prompt])
            print(f"✓ Response received from Gemini")
            
            if not response or not response.text:
                print("⚠️  Empty response from Gemini")
                return []
            
            # Parse JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            sections = json.loads(response_text)
            
            if not isinstance(sections, list):
                print(f"⚠️  Expected list, got {type(sections)}")
                return []
            
            print(f"✓ Extracted {len(sections)} legal sections from chunk {chunk_num}")
            
            # Debug: Print first section if available
            if sections:
                print(f"  Example: {sections[0].get('section_number', 'N/A')} - {sections[0].get('title', 'N/A')}")
            
            return sections
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error for chunk {chunk_num}: {e}")
            print(f"   Response: {response.text[:200]}...")
            return []
        except Exception as e:
            print(f"❌ Error processing chunk {chunk_num}: {e}")
            return []
    
    def process_file(self, file_path: Path) -> List[Dict[str, str]]:
        """Process a single file (PDF or PPTX)"""
        print(f"\n{'=' * 70}")
        print(f"PROCESSING FILE: {file_path.name}")
        print(f"{'=' * 70}")
        
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() == '.pptx':
            text = self.extract_text_from_pptx(file_path)
        else:
            print(f"⚠️  Unsupported file type: {file_path.suffix}")
            return []
        
        if not text:
            print(f"⚠️  No text extracted from {file_path.name}")
            return []
        
        # Split into chunks
        chunks = self.chunk_text(text)
        
        # Process each chunk with Gemini
        all_sections = []
        for i, chunk in enumerate(chunks, 1):
            print(f"\n--- Processing Chunk {i}/{len(chunks)} ---")
            sections = self.extract_legal_sections_from_chunk(chunk, i)
            all_sections.extend(sections)
        
        print(f"\n✓ Finished processing {file_path.name}")
        print(f"✓ Total sections extracted: {len(all_sections)}")
        
        return all_sections
    
    def process_all_files(self):
        """Process all PDF and PPTX files in the documents folder"""
        print(f"\n{'=' * 70}")
        print(f"SCANNING FOLDER: {self.documents_folder}")
        print(f"{'=' * 70}")
        
        # Find all PDF and PPTX files
        pdf_files = list(self.documents_folder.glob("*.pdf"))
        pptx_files = list(self.documents_folder.glob("*.pptx"))
        
        all_files = pdf_files + pptx_files
        
        print(f"✓ Found {len(pdf_files)} PDF files")
        print(f"✓ Found {len(pptx_files)} PPTX files")
        print(f"✓ Total files to process: {len(all_files)}")
        
        if not all_files:
            print("\n⚠️  No PDF or PPTX files found in folder")
            return
        
        # Process each file
        for file_path in all_files:
            sections = self.process_file(file_path)
            self.all_sections.extend(sections)
        
        print(f"\n{'=' * 70}")
        print(f"ALL FILES PROCESSED")
        print(f"{'=' * 70}")
        print(f"✓ Total legal sections extracted: {len(self.all_sections)}")
    
    def save_knowledge_base(self, output_path: str = "legal_knowledge.json"):
        """Save extracted sections to JSON file (appends to existing)"""
        print(f"\n{'=' * 70}")
        print(f"SAVING KNOWLEDGE BASE")
        print(f"{'=' * 70}")
        
        output_file = Path(output_path)
        
        # Load existing knowledge base if it exists
        existing_sections = {}
        if output_file.exists():
            print(f"✓ Found existing knowledge base: {output_file.name}")
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    existing_list = existing_data.get('legal_sections', [])
                    
                    # Convert to dict for deduplication
                    for section in existing_list:
                        section_num = section.get('section_number', '')
                        if section_num:
                            existing_sections[section_num] = section
                    
                    print(f"✓ Loaded {len(existing_sections)} existing sections")
            except Exception as e:
                print(f"⚠️  Could not load existing file: {e}")
                print("   Creating new knowledge base...")
        else:
            print(f"✓ Creating new knowledge base: {output_file.name}")
        
        # Add new sections (existing sections take precedence to preserve original data)
        new_count = 0
        for section in self.all_sections:
            section_num = section.get('section_number', '')
            if section_num and section_num not in existing_sections:
                existing_sections[section_num] = section
                new_count += 1
        
        print(f"✓ Added {new_count} new sections")
        print(f"✓ Total unique sections: {len(existing_sections)}")
        
        # Create final structure
        knowledge_base = {
            "legal_sections": list(existing_sections.values()),
            "total_sections": len(existing_sections),
            "extraction_method": "gemini-2.5-flash",
            "source": "Extracted from PDF and PPTX documents"
        }
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved knowledge base with {len(existing_sections)} sections")
        print(f"✓ Output file: {output_file.absolute()}")
        print(f"✓ File size: {output_file.stat().st_size / 1024:.2f} KB")
        
        # Print sample sections (show newly added ones if available)
        if new_count > 0:
            print(f"\n📋 Sample of newly added sections:")
            new_sections = [s for s in self.all_sections if s.get('section_number') in 
                          [sec.get('section_number') for sec in self.all_sections]]
            for i, section in enumerate(new_sections[:3], 1):
                print(f"\n  {i}. {section.get('section_number', 'N/A')}")
                print(f"     Title: {section.get('title', 'N/A')}")
                print(f"     Explanation: {section.get('explanation', 'N/A')[:100]}...")
        elif existing_sections:
            print(f"\n📋 Sample sections from knowledge base:")
            for i, section in enumerate(list(existing_sections.values())[:3], 1):
                print(f"\n  {i}. {section.get('section_number', 'N/A')}")
                print(f"     Title: {section.get('title', 'N/A')}")
                print(f"     Explanation: {section.get('explanation', 'N/A')[:100]}...")
        
        print(f"\n{'=' * 70}")
        print(f"✓ EXTRACTION COMPLETE!")
        print(f"{'=' * 70}\n")


def main():
    """Main execution function"""
    # Default documents folder (can be changed)
    documents_folder = Path(__file__).parent.parent / "documents"
    
    # Allow custom folder via command line
    if len(sys.argv) > 1:
        documents_folder = Path(sys.argv[1])
    
    # Create folder if it doesn't exist
    documents_folder.mkdir(exist_ok=True)
    
    print("\n" + "=" * 70)
    print("LEGAL KNOWLEDGE EXTRACTOR - GEMINI 2.5 FLASH")
    print("=" * 70)
    print(f"Documents folder: {documents_folder.absolute()}")
    print("=" * 70)
    
    # Initialize extractor
    extractor = LegalKnowledgeExtractor(str(documents_folder))
    
    # Process all files
    extractor.process_all_files()
    
    # Save knowledge base
    output_path = Path(__file__).parent.parent / "knowledge_base" / "legal_knowledge.json"
    output_path.parent.mkdir(exist_ok=True)
    
    extractor.save_knowledge_base(str(output_path))


if __name__ == "__main__":
    main()
