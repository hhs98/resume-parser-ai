# Resume Parser AI

A Python command-line tool that extracts structured information from PDF resumes using AI/ML models. Supports both OpenAI API and open source models via Ollama.

## Features

- Extracts comprehensive information from PDF resumes:
  - Personal information (name, email, phone, address, LinkedIn, GitHub)
  - Work experience (company, position, dates, description)
  - Education (institution, degree, field, dates, GPA)
  - Skills (technical and soft skills)
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
```

### Parse with Specific Options

```bash
# Using Ollama (default)
python -m src.cli parse resume.pdf --provider ollama --model llama3

# Using OpenAI
python -m src.cli parse resume.pdf --provider openai --model gpt-4o-mini --api-key YOUR_API_KEY

# Save to file
python -m src.cli parse resume.pdf --output result.json
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
- `--output` / `-o`: Output file path (default: stdout)
- `--format`: Output format (currently only `json`)
- `--api-key`: OpenAI API key (overrides environment variable)
- `--ollama-base-url`: Ollama server URL (default: `http://localhost:11434`)

## Output Format

The tool outputs structured JSON with the following schema:

```json
{
  "personal_info": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-234-567-8900",
    "address": "123 Main St, City, State",
    "linkedin": "https://linkedin.com/in/johndoe",
    "github": "https://github.com/johndoe"
  },
  "work_experience": [
    {
      "company": "Tech Corp",
      "position": "Software Engineer",
      "start_date": "2020-01",
      "end_date": "Present",
      "description": "Developed and maintained web applications..."
    }
  ],
  "education": [
    {
      "institution": "University of Example",
      "degree": "Bachelor of Science",
      "field": "Computer Science",
      "start_date": "2016-09",
      "end_date": "2020-05",
      "gpa": "3.8"
    }
  ],
  "skills": {
    "technical": ["Python", "JavaScript", "React", "Node.js"],
    "soft": ["Communication", "Leadership", "Problem Solving"]
  }
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

