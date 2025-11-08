# Resume Parser AI

A Python command-line tool that extracts structured information from PDF resumes using AI/ML models. Supports both OpenAI API and open source models via Ollama.

## Features

- Extracts comprehensive information aligned with your database schema:
  - User info (full name, DOB, gender, email, phone number)
  - Addresses (present and permanent)
  - Academic education (JSC/SSC/HSC/O & A levels + tertiary programs)
  - Employment history (company details, tenure, responsibilities)
  - Skills list
- Supports multiple AI providers:
  - **Ollama** (default) - Free, open source models running locally
  - **OpenAI** - Proprietary API with high accuracy
- Batch processing for multiple resumes
- JSON output format

## Installation

### Prerequisites

- Python 3.8 or higher
- For Ollama provider: [Ollama](https://ollama.ai/) installed and running

### Setup

1. Clone or navigate to the project directory:
```bash
cd resume-parser-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) For OpenAI provider, create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. (Optional) For Ollama provider, pull a model:
```bash
ollama pull llama3
# or
ollama pull mistral
```

## Usage

### Parse a Single Resume

```bash
python -m src.cli parse resume.pdf
# Creates resume.json in the same folder as the PDF
```

### Parse with Specific Options

```bash
# Using Ollama (default)
python -m src.cli parse resume.pdf --provider ollama --model llama3

# Using OpenAI
python -m src.cli parse resume.pdf --provider openai --model gpt-4o-mini --api-key YOUR_API_KEY

# Custom output location
python -m src.cli parse resume.pdf --output ./results/resume.json
```

### Batch Processing

```bash
# Parse all PDFs in a directory
python -m src.cli parse-batch ./resumes/

# Save results to a different directory
python -m src.cli parse-batch ./resumes/ --output ./results/
```

### Command-Line Options

- `--provider`: AI provider (`ollama` or `openai`, default: `ollama`)
- `--model`: Model name (default: `llama3` for Ollama, `gpt-4o-mini` for OpenAI)
- `--output` / `-o`: Output file path (default: `<input_filename>.json` next to the PDF)
- `--format`: Output format (currently only `json`)
- `--api-key`: OpenAI API key (overrides environment variable)
- `--ollama-base-url`: Ollama server URL (default: `http://localhost:11434`)

## Output Format

The tool outputs structured JSON with the following schema:

```json
{
  "user_info": {
    "name": "John Doe",
    "date_of_birth": "1995-04-12",
    "gender": "male",
    "email": "john.doe@example.com",
    "phone_number": "+8801700000000"
  },
  "addresses": [
    {
      "type": "present",
      "address": "123 Main Street, Dhaka",
      "post_name": "Dhanmondi",
      "post_code": "1209"
    },
    {
      "type": "permanent",
      "address": "Village Road, Chittagong",
      "post_name": "Mirsharai",
      "post_code": "4320"
    }
  ],
  "academic_education": [
    {
      "levels": "ssc",
      "subject": "Science",
      "board": "Dhaka",
      "institute": "ABC High School",
      "passing_year": "2012",
      "result": "GPA 5.00"
    },
    {
      "levels": "bachelors",
      "subject": "Computer Science",
      "board": "",
      "institute": "University of Example",
      "passing_year": "2018",
      "result": "CGPA 3.72"
    }
  ],
  "employment": [
    {
      "company_name": "Tech Corp",
      "company_type": "Software",
      "position": "Software Engineer",
      "joining_date": "2019-01-15",
      "leaving_date": "",
      "currently_working": true,
      "responsibility": "Developed and maintained web applications."
    }
  ],
  "skills": ["Python", "Django", "REST APIs", "React"]
}
```

## Model Recommendations

### Ollama (Open Source)

- **llama3** (recommended) - Good balance of speed and accuracy
- **mistral** - Fast and efficient
- **llama3.2** - Latest Llama model

### OpenAI

- **gpt-4o-mini** (recommended) - Cost-effective with good accuracy
- **gpt-4** - Highest accuracy (more expensive)
- **gpt-3.5-turbo** - Fast and cheaper option

## Troubleshooting

### Ollama Connection Issues

If you get connection errors, ensure Ollama is running:
```bash
ollama serve
```

Check if models are available:
```bash
ollama list
```

### OpenAI API Issues

Ensure your API key is set:
```bash
export OPENAI_API_KEY=your_key_here
```

Or use the `--api-key` option.

### PDF Extraction Issues

- Ensure the PDF is not password-protected
- Check that the PDF contains actual text (not just images)
- For scanned PDFs, use OCR tools first

## Development

### Project Structure

```
resume-parser-ai/
├── src/
│   ├── __init__.py
│   ├── parser.py              # Main parsing orchestrator
│   ├── pdf_extractor.py       # PDF text extraction
│   ├── ai_extractor/          # AI extraction modules
│   │   ├── base.py
│   │   ├── ollama_extractor.py
│   │   ├── openai_extractor.py
│   │   └── factory.py
│   └── cli.py                 # Command-line interface
├── requirements.txt
├── .env.example
└── README.md
```

## License

MIT

