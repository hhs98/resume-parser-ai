"""Base class for AI extractors."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class AIExtractor(ABC):
    """Abstract base class for AI-based information extraction."""
    
    @abstractmethod
    def extract(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract structured information from resume text.
        
        Args:
            resume_text: Raw text extracted from PDF
            
        Returns:
            Dictionary containing structured resume information
        """
        pass
    
    def _get_extraction_prompt(self, resume_text: str) -> str:
        """
        Generate the prompt for extracting resume information.
        
        Args:
            resume_text: Raw text extracted from PDF
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Extract structured information from the following resume text. 
Return the result as a valid JSON object with the following structure:

{{
  "personal_info": {{
    "name": "full name",
    "email": "email address",
    "phone": "phone number",
    "address": "full address if available",
    "linkedin": "LinkedIn URL if available",
    "github": "GitHub URL if available"
  }},
  "work_experience": [
    {{
      "company": "company name",
      "position": "job title",
      "start_date": "start date",
      "end_date": "end date or 'Present'",
      "description": "job description and responsibilities"
    }}
  ],
  "education": [
    {{
      "institution": "school/university name",
      "degree": "degree name",
      "field": "field of study",
      "start_date": "start date",
      "end_date": "graduation date",
      "gpa": "GPA if available"
    }}
  ],
  "skills": {{
    "technical": ["skill1", "skill2", ...],
    "soft": ["skill1", "skill2", ...]
  }}
}}

Resume text:
{resume_text}

Return only the JSON object, no additional text or explanation."""
        return prompt

