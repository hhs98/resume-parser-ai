"""OpenAI-based AI extractor."""

import json
from openai import OpenAI
from typing import Dict, Any, Optional
from .base import AIExtractor


class OpenAIExtractor(AIExtractor):
    """Extract information using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize OpenAI extractor.
        
        Args:
            api_key: OpenAI API key (if None, reads from environment)
            model: Model name (e.g., gpt-4, gpt-4o-mini, gpt-3.5-turbo)
        """
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    def extract(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract structured information using OpenAI.
        
        Args:
            resume_text: Raw text extracted from PDF
            
        Returns:
            Dictionary containing structured resume information
            
        Raises:
            ValueError: If API key is missing or extraction fails
            Exception: For API errors
        """
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        prompt = self._get_extraction_prompt(resume_text)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a resume parser. Extract structured information from resumes and return valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},  # Force JSON mode
                temperature=0.1  # Lower temperature for consistent output
            )
            
            response_text = response.choices[0].message.content
            
            # Parse JSON response
            parsed_data = json.loads(response_text)
            return parsed_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from OpenAI response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error during OpenAI extraction: {str(e)}")

