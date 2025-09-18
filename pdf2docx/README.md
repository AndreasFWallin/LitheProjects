# PDF to DOCX Converter CLI

A simple and powerful command-line tool for converting PDF files to DOCX format by extracting text.

## Features

- 🚀 **Batch conversion** - Convert multiple PDF files at once
- 📁 **Recursive processing** - Process subdirectories
- 📊 **Progress tracking** - Real-time conversion progress
- 🖥️ **Cross-platform** - Works on Windows, macOS, and Linux
- 📂 **Organized output** - Optional organized folder structure
- 🔄 **Overwrite protection** - Safe conversion with conflict handling
- 🗂️ **GUI support** - Optional GUI folder picker

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install PyPDF2 python-docx click
```

## Usage

### Basic Usage

Convert all PDF files in current directory:
```bash
python pdf2docx.py
```

Convert all PDF files in specific folder:
```bash
python pdf2docx.py /path/to/pdfs
```

### Advanced Usage

Convert with custom output folder:
```bash
python pdf2docx.py /path/to/pdfs --output /path/to/output
```

Convert recursively (including subdirectories):
```bash
python pdf2docx.py /path/to/pdfs --recursive
```

Use GUI folder picker:
```bash
python pdf2docx.py --gui
```

### Full Command Options

```bash
python pdf2docx.py [FOLDER_PATH] [OPTIONS]

Options:
  -o, --output PATH       Output directory for DOCX files
  -r, --recursive         Process subdirectories recursively
  -g, --gui               Use GUI folder picker
  -l, --list-only         Show what would be converted without doing it
  --help                  Show this message and exit
```

## Output Naming

The tool uses intelligent naming:

- **Standard**: `document.pdf` → `document.docx`
- **Conflict handling**: Skips if DOCX exists and is newer

## Error Handling

- **Corrupted PDFs**: Skips with warning
- **Permission errors**: Reports access issues
- **Text extraction**: Handles PDFs with or without extractable text

## Troubleshooting

### Common Issues

1. **"No PDF files found"**
   - Ensure the folder contains .pdf files
   - Check file extensions (case-insensitive)

2. **"Permission denied"**
   - Check read/write permissions
   - On macOS/Linux: `chmod +x pdf2docx.py`

3. **"Module not found"**
   - Install dependencies: `pip install -r requirements.txt`

## License

MIT License - feel free to use and modify as needed.