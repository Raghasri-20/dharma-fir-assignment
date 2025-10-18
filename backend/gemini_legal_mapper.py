"""
Gemini-based legal section mapper
Maps FIR text and entities to legal sections using Gemini AI with legal knowledge base context
"""
import json
import logging
from typing import Dict, List, Any
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiLegalMapper:
    """Map FIR to legal sections using Gemini with knowledge base context"""
    
    def __init__(self, model):
        self.model = model
        print("✓ Gemini Legal Mapper initialized")
    
    def map_to_legal_sections(
        self, 
        fir_text: str, 
        entities: Dict[str, List[str]], 
        legal_context: str
    ) -> List[Dict[str, str]]:
        """
        Map FIR text and entities to legal sections using Gemini
        
        Args:
            fir_text: Original FIR text
            entities: Extracted entities (names, crimes, threats, etc.)
            legal_context: Formatted legal knowledge base
            
        Returns:
            List of matched legal sections with section_number, title, explanation
        """
        print("\n🔍 Mapping FIR to legal sections using Gemini...")
        
        # Build comprehensive prompt with legal context
        prompt = self._build_mapping_prompt(fir_text, entities, legal_context)
        
        print("📤 Prompt sent to Gemini...")
        logger.info("Sending legal mapping prompt to Gemini")
        
        try:
            # Set request timeout and retry configuration
            response = self.model.generate_content(
                [prompt],
                request_options={"timeout": 45}  # 45 second timeout for Gemini API
            )
            print("✓ Response received from Gemini")
            logger.info("Received legal mapping response from Gemini")
            
            if not response or not response.text:
                print("⚠️  Empty response from Gemini")
                logger.warning("Empty response from Gemini for legal mapping")
                return []
            
            # Parse JSON response
            legal_sections = self._parse_response(response.text)
            
            print(f"✓ Initial extraction: {len(legal_sections)} sections matched")
            logger.info(f"Initially mapped {len(legal_sections)} legal sections")
            
            # Post-process: Remove duplicates and refine using Gemini
            if legal_sections and len(legal_sections) > 0:
                print("\n🔄 Post-processing: Removing duplicates and refining...")
                legal_sections = self._refine_sections(legal_sections, fir_text)
                print(f"✓ After refinement: {len(legal_sections)} unique sections")
            
            # Debug: Print first matched section
            if legal_sections:
                first = legal_sections[0]
                print(f"  Example: {first.get('section_number', 'N/A')} - {first.get('title', 'N/A')}")
            
            print(f"✓ Legal mapping complete: {len(legal_sections)} final sections")
            logger.info(f"Final mapped sections: {len(legal_sections)}")
            
            return legal_sections
            
        except Exception as e:
            print(f"❌ Error in legal mapping: {e}")
            logger.error(f"Error in Gemini legal mapping: {e}")
            return []
    
    def _build_mapping_prompt(
        self, 
        fir_text: str, 
        entities: Dict[str, List[str]], 
        legal_context: str
    ) -> str:
        """Build comprehensive prompt for legal section mapping"""
        
        # Format entities for prompt (compact format)
        entities_str = ", ".join([f"{k}: {v}" for k, v in entities.items() if v])
        
        # Optimize legal context - keep only first 30 sections to reduce prompt size
        context_lines = legal_context.split('\n')
        if len(context_lines) > 30:
            legal_context = '\n'.join(context_lines[:30])
            legal_context += f"\n... ({len(context_lines) - 30} more sections available)"
        
        print(f"📊 Prompt stats: FIR={len(fir_text)} chars, Context={len(legal_context)} chars")
        
        prompt = f"""Analyze this FIR and match it to relevant Indian legal sections.

FIR: {fir_text}

Entities: {entities_str}

Legal Sections:
{legal_context}

Return JSON array of 3-8 most relevant sections. Format:
[{{"section_number": "IPC Section 302", "title": "Murder", "explanation": "Why it applies"}}]

Rules:
- Only clearly relevant sections
- Use exact section numbers from above
- Return ONLY JSON array
- Empty array [] if no matches

JSON:"""

        return prompt
    
    def _refine_sections(self, sections: List[Dict[str, str]], fir_text: str) -> List[Dict[str, str]]:
        """
        Send extracted sections back to Gemini for deduplication and refinement
        Removes repetitive sections and improves explanations
        """
        print("📤 Sending sections to Gemini for refinement...")
        
        # Format sections for refinement prompt
        sections_json = json.dumps(sections, indent=2)
        
        refine_prompt = f"""You are a legal expert reviewing extracted legal sections for an FIR.

FIR Text:
{fir_text}

Extracted Legal Sections (may contain duplicates or irrelevant sections):
{sections_json}

Task:
1. Remove duplicate sections (same section number mentioned multiple times)
2. Remove sections that are NOT clearly relevant to this specific FIR
3. Keep only the most applicable sections (3-8 sections maximum)
4. Improve explanations to be specific to this FIR case
5. Ensure section numbers are accurate and properly formatted

Return a refined JSON array with unique, relevant sections only.

Rules:
- Remove exact duplicates (same section_number)
- Remove similar/overlapping sections (keep most specific one)
- Keep only sections that DIRECTLY apply to this FIR
- Improve explanations to reference specific FIR details
- Return ONLY JSON array, no additional text

Refined JSON:"""

        try:
            response = self.model.generate_content(
                [refine_prompt],
                request_options={"timeout": 30}
            )
            
            print("✓ Refinement response received")
            
            if not response or not response.text:
                print("⚠️  Empty refinement response, returning original sections")
                return sections
            
            # Parse refined response
            refined_sections = self._parse_response(response.text)
            
            if refined_sections and len(refined_sections) > 0:
                print(f"✓ Refined from {len(sections)} to {len(refined_sections)} sections")
                return refined_sections
            else:
                print("⚠️  Refinement returned empty, keeping original sections")
                return sections
                
        except Exception as e:
            print(f"⚠️  Refinement failed: {e}, keeping original sections")
            logger.warning(f"Section refinement failed: {e}")
            return sections
    
    def _parse_response(self, response_text: str) -> List[Dict[str, str]]:
        """Parse Gemini's JSON response"""
        try:
            # Clean response text
            response_text = response_text.strip()
            
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
                logger.warning(f"Unexpected response type: {type(sections)}")
                return []
            
            # Validate structure
            valid_sections = []
            for section in sections:
                if isinstance(section, dict) and \
                   'section_number' in section and \
                   'title' in section and \
                   'explanation' in section:
                    valid_sections.append(section)
                else:
                    print(f"⚠️  Skipping invalid section: {section}")
            
            return valid_sections
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"   Response: {response_text[:200]}...")
            logger.error(f"JSON parsing error in legal mapping: {e}")
            return []
        except Exception as e:
            print(f"❌ Error parsing response: {e}")
            logger.error(f"Error parsing legal mapping response: {e}")
            return []


def create_gemini_legal_mapper(model) -> GeminiLegalMapper:
    """Factory function to create GeminiLegalMapper"""
    return GeminiLegalMapper(model)
