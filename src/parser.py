"""Main resume parser orchestrator."""

from typing import Dict, Any, Optional
from pathlib import Path

from .pdf_extractor import PDFExtractor
from .ai_extractor import AIExtractorFactory


class ResumeParser:
    """Main parser that orchestrates PDF extraction and AI-based information extraction."""
    
    def __init__(
        self,
        provider: str = "ollama",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        ollama_base_url: Optional[str] = None
    ):
        """
        Initialize the resume parser.
        
        Args:
            provider: AI provider ("ollama" or "openai")
            model: Model name (provider-specific)
            api_key: OpenAI API key (only needed for OpenAI provider)
            ollama_base_url: Ollama server base URL
        """
        self.pdf_extractor = PDFExtractor()
        self.ai_extractor = AIExtractorFactory.create(
            provider=provider,
            model=model,
            api_key=api_key,
            ollama_base_url=ollama_base_url
        )
    
    def parse(self, pdf_path: str) -> Dict[str, Any]:
        """
        Parse a resume PDF and extract structured information.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing structured resume information
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF extraction or AI extraction fails
            PermissionError: If PDF is password-protected
        """
        # Validate PDF file
        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Extract text from PDF
        try:
            resume_text = self.pdf_extractor.extract_text(pdf_path)
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
        
        # Validate that we got some text
        if not resume_text or len(resume_text.strip()) < 10:
            raise ValueError(f"Insufficient text extracted from PDF: {pdf_path}")
        
        # Extract structured information using AI
        try:
            structured_data = self.ai_extractor.extract(resume_text)
        except Exception as e:
            raise ValueError(f"Failed to extract information using AI: {str(e)}")
        
        # Validate and normalize the output structure
        normalized_data = self._normalize_output(structured_data)
        
        return normalized_data
    
    def _normalize_output(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize and validate the output structure.
        
        Args:
            data: Raw extracted data
            
        Returns:
            Normalized data structure
        """
        # Ensure all required top-level keys exist
        normalized = {
            "personal_info": data.get("personal_info", {}),
            "work_experience": data.get("work_experience", []),
            "education": data.get("education", []),
            "skills": data.get("skills", {})
        }
        
        # Ensure personal_info has expected fields
        personal_info = normalized["personal_info"]
        if not isinstance(personal_info, dict):
            personal_info = {}
        
        normalized["personal_info"] = {
            "name": personal_info.get("name", ""),
            "email": personal_info.get("email", ""),
            "phone": personal_info.get("phone", ""),
            "address": personal_info.get("address", ""),
            "linkedin": personal_info.get("linkedin", ""),
            "github": personal_info.get("github", "")
        }
        
        # Ensure work_experience is a list
        if not isinstance(normalized["work_experience"], list):
            normalized["work_experience"] = []
        
        # Ensure education is a list
        if not isinstance(normalized["education"], list):
            normalized["education"] = []
        
        # Ensure skills has technical and soft keys
        skills = normalized["skills"]
        if not isinstance(skills, dict):
            skills = {}
        
        normalized["skills"] = {
            "technical": skills.get("technical", []) if isinstance(skills.get("technical"), list) else [],
            "soft": skills.get("soft", []) if isinstance(skills.get("soft"), list) else []
        }
        
        return normalized

