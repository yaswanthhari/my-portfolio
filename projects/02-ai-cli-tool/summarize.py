#!/usr/bin/env python3
"""
AI Text Summarizer CLI Tool
Usage: summarize.py --file notes.txt --length short
"""

import os
os.environ['HF_HOME'] = 'D:/huggingface_cache'
import click
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import pyperclip
from datetime import datetime

class AISummarizer:
    """Handles AI summarization using local models"""
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        click.echo("✅ AI Model loaded", err=True)
    
    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """Generate summary with error handling"""
        try:
            # Truncate very long texts (model limit)
            if len(text) > 1024:
                text = text[:1024]
                click.echo("⚠️  Text truncated to 1024 chars", err=True)
            
            inputs = self.tokenizer("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = self.model.generate(
                inputs["input_ids"], 
                max_length=max_length, 
                min_length=min_length, 
                length_penalty=2.0, 
                num_beams=4, 
                early_stopping=True
            )
            return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_text_from_file(self, filepath: Path) -> str:
        """Read text from various file formats"""
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_text_from_clipboard(self) -> str:
        """Get text from system clipboard"""
        text = pyperclip.paste()
        if not text:
            raise ValueError("Clipboard is empty")
        return text

@click.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='Input file path')
@click.option('--clipboard', '-c', is_flag=True, help='Read from clipboard')
@click.option('--text', '-t', help='Direct text input')
@click.option('--max-length', default=130, help='Maximum summary length')
@click.option('--min-length', default=30, help='Minimum summary length')
@click.option('--output', '-o', type=click.Path(), help='Save summary to file')
@click.option('--model', default="facebook/bart-large-cnn", help='HuggingFace model')
def main(file, clipboard, text, max_length, min_length, output, model):
    """AI-Powered Text Summarizer CLI Tool"""
    
    click.echo("\n📝 AI Summarizer Tool\n" + "="*40)
    
    # Initialize summarizer
    with click.progressbar(length=1, label='Loading AI model') as bar:
        summarizer = AISummarizer(model)
        bar.update(1)
    
    # Get input text
    input_text = None
    if file:
        click.echo(f"📄 Reading from file: {file}")
        input_text = summarizer.get_text_from_file(Path(file))
    elif clipboard:
        click.echo("📋 Reading from clipboard")
        input_text = summarizer.get_text_from_clipboard()
    elif text:
        click.echo("✍️ Using direct text input")
        input_text = text
    else:
        # Read from stdin (pipe)
        if not sys.stdin.isatty():
            click.echo("📥 Reading from stdin")
            input_text = sys.stdin.read()
        else:
            click.echo("❌ No input provided. Use --file, --clipboard, --text, or pipe input")
            sys.exit(1)
    
    # Validate input
    if not input_text or len(input_text.strip()) < 20:
        click.echo("❌ Text too short to summarize (min 20 characters)")
        sys.exit(1)
    
    click.echo(f"📊 Original text length: {len(input_text)} chars")
    
    # Generate summary
    with click.progressbar(length=1, label='Generating summary') as bar:
        summary = summarizer.summarize(input_text, max_length, min_length)
        bar.update(1)
    
    # Display results
    click.echo("\n" + "="*40)
    click.echo("✨ SUMMARY:")
    click.echo("="*40)
    click.echo(summary)
    click.echo("="*40)
    
    # Save to file if requested
    if output:
        output_path = Path(output)
        output_path.write_text(f"Original: {input_text[:200]}...\n\nSummary: {summary}")
        click.echo(f"💾 Summary saved to: {output_path}")
    
    # Copy to clipboard option (optional)
    if click.confirm('\n📋 Copy summary to clipboard?'):
        pyperclip.copy(summary)
        click.echo("✅ Copied to clipboard!")

if __name__ == "__main__":
    main()
