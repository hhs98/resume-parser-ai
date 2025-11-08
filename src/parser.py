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
        normalized = {
            "user_info": self._normalize_user_info(data.get("user_info", {})),
            "addresses": self._normalize_addresses(data.get("addresses", [])),
            "academic_education": self._normalize_academic_education(data.get("academic_education", [])),
            "employment": self._normalize_employment(data.get("employment", [])),
            "skills": self._normalize_skills(data.get("skills", []))
        }
        
        return normalized

    def _normalize_user_info(self, user_info: Any) -> Dict[str, str]:
        if not isinstance(user_info, dict):
            user_info = {}
        return {
            "name": user_info.get("name", "") or "",
            "date_of_birth": user_info.get("date_of_birth", "") or "",
            "gender": user_info.get("gender", "") or "",
            "email": user_info.get("email", "") or "",
            "phone_number": user_info.get("phone_number", "") or ""
        }

    def _normalize_addresses(self, addresses: Any) -> list:
        if not isinstance(addresses, list):
            addresses = []
        normalized_addresses = []
        for address in addresses:
            if not isinstance(address, dict):
                continue
            normalized_addresses.append({
                "type": (address.get("type") or "").lower(),
                "address": address.get("address", "") or "",
                "post_name": address.get("post_name", "") or "",
                "post_code": address.get("post_code", "") or ""
            })
        return normalized_addresses

    def _normalize_academic_education(self, entries: Any) -> list:
        if not isinstance(entries, list):
            entries = []
        normalized_entries = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            normalized_entries.append({
                "levels": (entry.get("levels") or "").lower(),
                "subject": entry.get("subject", "") or "",
                "board": entry.get("board", "") or "",
                "institute": entry.get("institute", "") or "",
                "passing_year": entry.get("passing_year", "") or "",
                "result": entry.get("result", "") or ""
            })
        return normalized_entries

    def _normalize_employment(self, entries: Any) -> list:
        if not isinstance(entries, list):
            entries = []
        normalized_entries = []
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            currently_working = entry.get("currently_working", False)
            if isinstance(currently_working, str):
                currently_working = currently_working.strip().lower() in {"yes", "true", "1"}
            normalized_entries.append({
                "company_name": entry.get("company_name", "") or "",
                "company_type": entry.get("company_type", "") or "",
                "position": entry.get("position", "") or "",
                "joining_date": entry.get("joining_date", "") or "",
                "leaving_date": entry.get("leaving_date", "") or "",
                "currently_working": bool(currently_working),
                "responsibility": entry.get("responsibility", "") or ""
            })
        return normalized_entries

    def _normalize_skills(self, skills: Any) -> list:
        if isinstance(skills, dict):
            # Flatten values if provided as categories
            values = []
            for value in skills.values():
                if isinstance(value, list):
                    values.extend(value)
            skills = values
        if not isinstance(skills, list):
            skills = []
        normalized_skills = []
        for skill in skills:
            if isinstance(skill, str):
                normalized_skills.append(skill.strip())
            elif isinstance(skill, dict) and "name" in skill:
                normalized_skills.append(str(skill.get("name") or "").strip())
        return [s for s in normalized_skills if s]

