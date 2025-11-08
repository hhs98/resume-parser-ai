"""Command-line interface for resume parser."""

import json
import sys
import click
from pathlib import Path
from typing import Optional

from .parser import ResumeParser


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Resume Parser AI - Extract structured information from PDF resumes."""
    pass


@cli.command()
@click.argument("pdf_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output", "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="Output file path (default: <input_filename>.json in same directory)"
)
@click.option(
    "--format",
    type=click.Choice(["json"], case_sensitive=False),
    default="json",
    help="Output format (default: json)"
)
@click.option(
    "--provider",
    type=click.Choice(["ollama", "openai"], case_sensitive=False),
    default="ollama",
    help="AI provider (default: ollama)"
)
@click.option(
    "--model",
    type=str,
    default=None,
    help="Model name (default: llama3 for ollama, gpt-4o-mini for openai)"
)
@click.option(
    "--api-key",
    type=str,
    default=None,
    help="OpenAI API key (overrides environment variable)"
)
@click.option(
    "--ollama-base-url",
    type=str,
    default=None,
    help="Ollama server URL (default: http://localhost:11434)"
)
def parse(pdf_file: Path, output: Optional[Path], format: str, provider: str, 
          model: Optional[str], api_key: Optional[str], ollama_base_url: Optional[str]):
    """Parse a single resume PDF file."""
    try:
        # Initialize parser
        parser = ResumeParser(
            provider=provider,
            model=model,
            api_key=api_key,
            ollama_base_url=ollama_base_url
        )
        
        # Parse the resume
        click.echo(f"Parsing resume: {pdf_file}", err=True)
        result = parser.parse(str(pdf_file))
        
        # Format output
        if format.lower() == "json":
            output_text = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            output_text = json.dumps(result, indent=2, ensure_ascii=False)
        
        # Determine output file path
        if output:
            output_path = output
        else:
            # Auto-generate output filename based on input PDF
            output_path = pdf_file.parent / f"{pdf_file.stem}.json"
        
        # Write output to file
        output_path.write_text(output_text, encoding='utf-8')
        click.echo(f"Results saved to: {output_path}", err=True)
        
    except FileNotFoundError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except PermissionError as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option(
    "--output", "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="Output directory path (default: same as input directory)"
)
@click.option(
    "--format",
    type=click.Choice(["json"], case_sensitive=False),
    default="json",
    help="Output format (default: json)"
)
@click.option(
    "--provider",
    type=click.Choice(["ollama", "openai"], case_sensitive=False),
    default="ollama",
    help="AI provider (default: ollama)"
)
@click.option(
    "--model",
    type=str,
    default=None,
    help="Model name (default: llama3 for ollama, gpt-4o-mini for openai)"
)
@click.option(
    "--api-key",
    type=str,
    default=None,
    help="OpenAI API key (overrides environment variable)"
)
@click.option(
    "--ollama-base-url",
    type=str,
    default=None,
    help="Ollama server URL (default: http://localhost:11434)"
)
def parse_batch(directory: Path, output: Optional[Path], format: str, provider: str,
                model: Optional[str], api_key: Optional[str], ollama_base_url: Optional[str]):
    """Parse multiple resume PDF files from a directory."""
    # Find all PDF files
    pdf_files = list(directory.glob("*.pdf"))
    
    if not pdf_files:
        click.echo(f"No PDF files found in directory: {directory}", err=True)
        sys.exit(1)
    
    # Determine output directory
    if output is None:
        output_dir = directory
    else:
        output_dir = output
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize parser
    parser = ResumeParser(
        provider=provider,
        model=model,
        api_key=api_key,
        ollama_base_url=ollama_base_url
    )
    
    # Process each file
    successful = 0
    failed = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        try:
            click.echo(f"[{i}/{len(pdf_files)}] Parsing: {pdf_file.name}", err=True)
            result = parser.parse(str(pdf_file))
            
            # Generate output filename
            output_filename = pdf_file.stem + ".json"
            output_path = output_dir / output_filename
            
            # Format and save output
            output_text = json.dumps(result, indent=2, ensure_ascii=False)
            output_path.write_text(output_text, encoding='utf-8')
            
            successful += 1
            click.echo(f"  ✓ Saved to: {output_path}", err=True)
            
        except Exception as e:
            failed += 1
            click.echo(f"  ✗ Failed: {str(e)}", err=True)
            continue
    
    # Summary
    click.echo(f"\nProcessed {len(pdf_files)} files:", err=True)
    click.echo(f"  Successful: {successful}", err=True)
    click.echo(f"  Failed: {failed}", err=True)


if __name__ == "__main__":
    cli()

