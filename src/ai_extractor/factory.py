"""Factory for creating AI extractor instances."""

from typing import Optional
import os
from dotenv import load_dotenv

from .base import AIExtractor
from .ollama_extractor import OllamaExtractor
from .openai_extractor import OpenAIExtractor

# Load environment variables
load_dotenv()


class AIExtractorFactory:
    """Factory for creating AI extractor instances."""
    
    @staticmethod
    def create(
        provider: str = "ollama",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        ollama_base_url: Optional[str] = None
    ) -> AIExtractor:
        """
        Create an AI extractor instance.
        
        Args:
            provider: Provider name ("ollama" or "openai")
            model: Model name (provider-specific)
            api_key: API key for OpenAI (optional, reads from env if not provided)
            ollama_base_url: Base URL for Ollama server (optional, defaults to localhost)
            
        Returns:
            AIExtractor instance
            
        Raises:
            ValueError: If provider is not supported
        """
        provider = provider.lower()
        
        if provider == "ollama":
            # Default model for Ollama
            if not model:
                model = "llama3"
            
            # Get Ollama base URL from parameter or environment
            base_url = ollama_base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            
            return OllamaExtractor(model=model, base_url=base_url)
        
        elif provider == "openai":
            # Default model for OpenAI
            if not model:
                model = "gpt-4o-mini"
            
            # Get API key from parameter or environment
            key = api_key or os.getenv("OPENAI_API_KEY")
            
            return OpenAIExtractor(api_key=key, model=model)
        
        else:
            raise ValueError(f"Unsupported provider: {provider}. Supported providers: ollama, openai")

