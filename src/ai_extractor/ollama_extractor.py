"""Ollama-based AI extractor."""

import json
import ollama
from typing import Dict, Any, Optional
from .base import AIExtractor


class OllamaExtractor(AIExtractor):
    """Extract information using Ollama open source models."""
    
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama extractor.
        
        Args:
            model: Model name (e.g., llama3, mistral, llama3.2)
            base_url: Ollama server base URL
        """
        self.model = model
        self.base_url = base_url
        self.client = ollama.Client(host=base_url)
    
    def extract(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract structured information using Ollama.
        
        Args:
            resume_text: Raw text extracted from PDF
            
        Returns:
            Dictionary containing structured resume information
            
        Raises:
            ConnectionError: If Ollama server is not reachable
            ValueError: If extraction fails or returns invalid JSON
        """
        try:
            # Check if Ollama server is available
            self._check_server_health()
        except Exception as e:
            raise ConnectionError(f"Ollama server not available at {self.base_url}: {str(e)}")
        
        prompt = self._get_extraction_prompt(resume_text)
        
        try:
            # Use chat completion for better structured output
            response = self.client.chat(
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
                options={
                    "temperature": 0.1,  # Lower temperature for more consistent JSON output
                    "format": "json"  # Request JSON format
                }
            )
            
            # Extract the response text
            # Ollama chat returns message content
            response_text = response.get('message', {}).get('content', '')
            if not response_text:
                # Fallback to direct response field
                response_text = response.get('response', '')
            
            # Try to parse JSON from response
            # Sometimes models return JSON wrapped in markdown code blocks
            json_text = self._extract_json_from_response(response_text)
            
            parsed_data = json.loads(json_text)
            return parsed_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from Ollama response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error during extraction: {str(e)}")
    
    def _check_server_health(self):
        """Check if Ollama server is running and accessible."""
        try:
            # Try to list models to verify server is up
            self.client.list()
        except Exception as e:
            raise ConnectionError(f"Cannot connect to Ollama server: {str(e)}")
    
    def _extract_json_from_response(self, response_text: str) -> str:
        """
        Extract JSON from response, handling cases where it's wrapped in markdown.
        
        Args:
            response_text: Raw response text
            
        Returns:
            JSON string
        """
        # Remove markdown code blocks if present
        if '```json' in response_text:
            start = response_text.find('```json') + 7
            end = response_text.find('```', start)
            if end != -1:
                return response_text[start:end].strip()
        elif '```' in response_text:
            start = response_text.find('```') + 3
            end = response_text.find('```', start)
            if end != -1:
                return response_text[start:end].strip()
        
        # Try to find JSON object boundaries
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start != -1 and end > start:
            return response_text[start:end]
        
        return response_text.strip()

