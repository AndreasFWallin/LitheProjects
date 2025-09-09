#!/usr/bin/env python3
"""
JPG to PNG Converter CLI Tool

A simple command-line tool for batch converting JPG images to PNG format with appropriate naming.
Usage: python jpg2png.py [folder_path] [options]
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import click
from PIL import Image
from typing import List
import tkinter as tk
from tkinter import filedialog

class ImageConverter:
    """Handles JPG to PNG conversion with progress tracking."""
    
    def __init__(self, target_folder: Path):
        self.target_folder = Path(target_folder)
        self.supported_extensions = {'.jpg', '.jpeg', '.JPG', '.JPEG'}
        self.converted_files = []
        
    def find_jpg_files(self) -> List[Path]:
        """Find all JPG files in the target folder."""
        jpg_files = []
        for ext in self.supported_extensions:
            jpg_files.extend(self.target_folder.glob(f'*{ext}'))
            jpg_files.extend(self.target_folder.glob(f'**/*{ext}'))  # Recursive
        
        return sorted(jpg_files)
    
    def get_png_filename(self, jpg_path: Path, prefix_format: str = None) -> Path:
        """Generate appropriate PNG filename based on options."""
        stem = jpg_path.stem
        
        if prefix_format == 'timestamp':
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return jpg_path.with_suffix('').parent / f"{timestamp}_{stem}.png"
        elif prefix_format == 'counter':
            counter = len(self.converted_files) + 1
            return jpg_path.with_suffix('').parent / f"converted_{counter:03d}_{stem}.png"
        elif prefix_format == 'batch':
            batch_name = self.target_folder.name
            return jpg_path.with_suffix('').parent / f"{batch_name}_{stem}.png"
        else:
            return jpg_path.with_suffix('.png')
    
    def convert_image(self, jpg_path: Path, output_path: Path, quality: int = 95) -> bool:
        """Convert a single JPG to PNG."""
        try:
            with Image.open(jpg_path) as img:
                if img.mode != 'RGBA' and 'transparency' in img.info:
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
                
                img.save(output_path, 'PNG', optimize=True, compress_level=quality)
                return True
                
        except Exception as e:
            click.echo(f"❌ Error converting {jpg_path.name}: {e}", err=True)
            return False
    
    def process_folder(self, output_folder: Path = None, prefix_format: str = None, 
                      recursive: bool = False, quality: int = 95) -> dict:
        """Process all JPG files in the folder."""
        if output_folder is None:
            output_folder = self.target_folder
        
        # Create output folder if it doesn't exist
        output_folder.mkdir(parents=True, exist_ok=True)
        
        jpg_files = self.find_jpg_files() if recursive else [f for f in self.target_folder.glob('*') 
                                                           if f.suffix.lower() in self.supported_extensions]
        
        if not jpg_files:
            return {'converted': 0, 'skipped': 0, 'files': []}
        
        results = {'converted': 0, 'skipped': 0, 'files': []}
        
        with click.progressbar(jpg_files, label='Converting images') as bar:
            for jpg_file in bar:
                png_path = self.get_png_filename(jpg_file, prefix_format)
                
                # Adjust path if output folder is specified
                if output_folder != self.target_folder:
                    png_path = output_folder / png_path.name
                
                # Skip if PNG already exists and is newer
                if png_path.exists() and png_path.stat().st_mtime > jpg_file.stat().st_mtime:
                    results['skipped'] += 1
                    continue
                
                if self.convert_image(jpg_file, png_path, quality):
                    results['converted'] += 1
                    results['files'].append(png_path)
                    self.converted_files.append(png_path)
        
        return results


@click.command()
@click.argument('folder_path', required=False, type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--output', '-o', type=click.Path(file_okay=False, dir_okay=True),
              help='Output folder for PNG files (default: same as input)')
@click.option('--prefix', '-p', 
              type=click.Choice(['none', 'timestamp', 'counter', 'batch'], case_sensitive=False),
              default='none', help='Naming prefix for output files')
@click.option('--recursive', '-r', is_flag=True, help='Search subdirectories recursively')
@click.option('--quality', '-q', default=9, type=click.IntRange(0, 9),
              help='PNG compression level (0-9, higher = better compression, slower)')
@click.option('--interactive', '-i', is_flag=True, help='Use GUI folder selector')
@click.option('--list-only', '-l', is_flag=True, help='Show what would be converted without doing it')
def main(folder_path, output, prefix, recursive, quality, interactive, list_only):
    """Convert JPG files in a folder to PNG format.
    
    Examples:
        jpg2png.py photos/
        jpg2png.py photos/ --output converted/ --prefix timestamp
        jpg2png.py --interactive --recursive
    """
    
    # Use GUI selector if requested
    if interactive or not folder_path:
        root = tk.Tk()
        root.withdraw()  # Hide main window
        root.attributes('-topmost', True)
        
        folder_path = filedialog.askdirectory(title="Select folder with JPG images")
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
    
    converter = ImageConverter(folder_path)
    jpg_files = converter.find_jpg_files() if recursive else [f for f in folder_path.glob('*') 
                                                           if f.suffix.lower() in {'.jpg', '.jpeg'}]
    
    if not jpg_files:
        click.echo("✅ No JPG files found in the specified folder.")
        return
    
    click.echo(f"📁 Found {len(jpg_files)} JPG file(s) to convert")
    
    if list_only:
        click.echo("Files that would be converted:")
        for file in jpg_files:
            click.echo(f"  {file.name} -> {converter.get_png_filename(file, prefix).name}")
        return
    
    # Convert files
    output_path = Path(output) if output else None
    results = converter.process_folder(output_path, prefix, recursive, 9-quality)
    
    # Summary
    click.echo("\n" + "="*50)
    click.echo(f"✅ Conversion complete!")
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