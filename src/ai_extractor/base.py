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
Return the result as a valid JSON object that matches this schema:

{{
  "user_info": {{
    "name": "",
    "date_of_birth": "YYYY-MM-DD or empty",
    "gender": "male|female|other",
    "email": "",
    "phone_number": ""
  }},
  "addresses": [
    {{
      "type": "present|permanent",
      "address": "full address line",
      "post_name": "",
      "post_code": ""
    }}
  ],
  "academic_education": [
    {{
      "levels": "jsc|ssc|hsc|o_level|a_level|bachelors|masters|phd|diploma|ca_qualified|ca_cc|cma_qualified|cma_student|acca|cs|mbbs|bds|llb|llm|other",
      "subject": "",
      "board": "",
      "institute": "",
      "passing_year": "",
      "result": ""
    }}
  ],
  "employment": [
    {{
      "company_name": "",
      "company_type": "",
      "position": "",
      "joining_date": "YYYY-MM-DD or empty",
      "leaving_date": "YYYY-MM-DD or empty",
      "currently_working": true,
      "responsibility": ""
    }}
  ],
  "skills": ["skill one", "skill two"]
}}

Guidelines:
- Fill missing values with empty strings.
- Use arrays even if there is only one item.
- Only include address types that appear in the resume.
- Use ISO date format when possible.

Resume text:
{resume_text}

Return only the JSON object, no additional text or explanation."""
        return prompt

