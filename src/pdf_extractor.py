"""PDF text extraction module."""

import pdfplumber
from pathlib import Path


class PDFExtractor:
    """Extracts text content from PDF files."""
    
    def __init__(self):
        """Initialize the PDF extractor."""
        pass
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a PDF or is corrupted
            PermissionError: If the PDF is password-protected
        """
        pdf_path_obj = Path(pdf_path)
        
        if not pdf_path_obj.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path_obj.suffix.lower() == '.pdf':
            raise ValueError(f"File is not a PDF: {pdf_path}")
        
        try:
            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
            
            if not text_content:
                raise ValueError(f"No text could be extracted from PDF: {pdf_path}")
            
            # Join all pages with newlines
            full_text = "\n\n".join(text_content)
            
            # Clean up excessive whitespace while preserving structure
            cleaned_text = self._clean_text(full_text)
            
            return cleaned_text
            
        except pdfplumber.PDFException as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
        except Exception as e:
            # Check if it's a password-protected PDF
            if "password" in str(e).lower() or "encrypted" in str(e).lower():
                raise PermissionError(f"PDF is password-protected: {pdf_path}")
            raise ValueError(f"Unexpected error extracting PDF: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing excessive whitespace.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        # Replace multiple newlines with double newline
        import re
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Replace multiple spaces with single space (but preserve newlines)
        text = re.sub(r'[ \t]+', ' ', text)
        # Remove leading/trailing whitespace from each line
        lines = [line.strip() for line in text.split('\n')]
        # Remove empty lines but preserve paragraph breaks
        cleaned_lines = []
        prev_empty = False
        for line in lines:
            if line:
                cleaned_lines.append(line)
                prev_empty = False
            elif not prev_empty:
                cleaned_lines.append('')
                prev_empty = True
        
        return '\n'.join(cleaned_lines).strip()

