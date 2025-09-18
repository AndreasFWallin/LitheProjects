#!/usr/bin/env python3
"""
PDF to DOCX Converter CLI Tool

A simple command-line tool for converting PDF files to DOCX format by extracting text.
Usage: python pdf2docx.py [folder_path] [options]
"""

import os
import sys
from pathlib import Path
from typing import List
import click
from PyPDF2 import PdfReader
from docx import Document
import tkinter as tk
from tkinter import filedialog

class PDFConverter:
    """Handles PDF to DOCX conversion with progress tracking."""
    
    def __init__(self, target_folder: Path):
        self.target_folder = Path(target_folder)
        self.supported_extensions = {'.pdf', '.PDF'}
        self.converted_files = []
        
    def find_pdf_files(self, recursive: bool = False) -> List[Path]:
        """Find all PDF files in the target folder."""
        pdf_files = []
        if recursive:
            for ext in self.supported_extensions:
                pdf_files.extend(self.target_folder.glob(f'**/*{ext}'))
        else:
            for ext in self.supported_extensions:
                pdf_files.extend(self.target_folder.glob(f'*{ext}'))
        
        return sorted(pdf_files)
    
    def get_docx_filename(self, pdf_path: Path) -> Path:
        """Generate DOCX filename from PDF path."""
        return pdf_path.with_suffix('.docx')
    
    def convert_pdf(self, pdf_path: Path, output_path: Path) -> bool:
        """Convert a single PDF to DOCX by extracting text."""
        try:
            reader = PdfReader(pdf_path)
            doc = Document()
            
            for page in reader.pages:
                text = page.extract_text()
                doc.add_paragraph(text)
            
            doc.save(output_path)
            return True
            
        except Exception as e:
            click.echo(f"❌ Error converting {pdf_path.name}: {e}", err=True)
            return False
    
    def process_folder(self, output_folder: Path = None, recursive: bool = False) -> dict:
        """Process all PDF files in the folder."""
        if output_folder is None:
            output_folder = self.target_folder
        
        # Create output folder if it doesn't exist
        output_folder.mkdir(parents=True, exist_ok=True)
        
        pdf_files = self.find_pdf_files(recursive)
        
        if not pdf_files:
            return {'converted': 0, 'skipped': 0, 'files': []}
        
        results = {'converted': 0, 'skipped': 0, 'files': []}
        
        with click.progressbar(pdf_files, label='Converting PDFs') as bar:
            for pdf_file in bar:
                docx_path = self.get_docx_filename(pdf_file)
                
                # Adjust path if output folder is specified
                if output_folder != self.target_folder:
                    docx_path = output_folder / docx_path.name
                
                # Skip if DOCX already exists and is newer
                if docx_path.exists() and docx_path.stat().st_mtime > pdf_file.stat().st_mtime:
                    results['skipped'] += 1
                    continue
                
                if self.convert_pdf(pdf_file, docx_path):
                    results['converted'] += 1
                    results['files'].append(docx_path)
                    self.converted_files.append(docx_path)
        
        return results

@click.command()
@click.argument('folder_path', required=False, type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output', '-o', type=click.Path(file_okay=False, dir_okay=True),
              help='Output folder for DOCX files (default: same as input)')
@click.option('--recursive', '-r', is_flag=True, help='Search subdirectories recursively')
@click.option('--interactive', '-i', is_flag=True, help='Use GUI folder selector')
@click.option('--list-only', '-l', is_flag=True, help='Show what would be converted without doing it')
def main(folder_path, output, recursive, interactive, list_only):
    """Convert PDF files in a folder to DOCX format.
    
    Examples:
        pdf2docx.py documents/
        pdf2docx.py documents/ --output converted/ --recursive
        pdf2docx.py --interactive
    """
    
    # Use GUI selector if requested
    if interactive or not folder_path:
        root = tk.Tk()
        root.withdraw()  # Hide main window
        root.attributes('-topmost', True)
        
        folder_path = filedialog.askdirectory(title="Select folder with PDF files")
        if not folder_path:
            click.echo("❌ No folder selected. Exiting.")
            return
    
    if not folder_path:
        click.echo("❌ Please provide a folder path or use --interactive mode")
        return
    
    folder_path = Path(folder_path)
    
    if not folder_path.exists() or not folder_path.is_dir():
        click.echo(f"❌ Error: {folder_path} is not a valid directory")
        return
    
    converter = PDFConverter(folder_path)
    pdf_files = converter.find_pdf_files(recursive)
    
    if not pdf_files:
        click.echo("✅ No PDF files found in the specified folder.")
        return
    
    click.echo(f"📁 Found {len(pdf_files)} PDF file(s) to convert")
    
    if list_only:
        click.echo("Files that would be converted:")
        for file in pdf_files:
            click.echo(f"  {file.name} -> {converter.get_docx_filename(file).name}")
        return
    
    # Convert files
    output_path = Path(output) if output else None
    results = converter.process_folder(output_path, recursive)
    
    # Summary
    click.echo("\n" + "="*50)
    click.echo("✅ Conversion complete!"
    click.echo(f"   📊 Converted: {results['converted']} file(s)")
    click.echo(f"   ⏭️  Skipped: {results['skipped']} file(s)")
    
    if results['files']:
        click.echo(f"\n📂 Output location: {output_path or folder_path}")
        click.echo("First few files:")
        for i, file in enumerate(results['files'][:3]):
            click.echo(f"  {i+1}. {file.name}")
        
        if len(results['files']) > 3:
            click.echo(f"  ... and {len(results['files']) - 3} more files")

if __name__ == '__main__':
    main()