# JPG to PNG Converter CLI

A simple and powerful command-line tool for batch converting JPG images to PNG format with intelligent naming and progress tracking.

## Features

- 🚀 **Batch conversion** - Convert multiple JPG files at once
- 🎯 **Smart naming** - Automatic PNG naming with timestamp support
- 📁 **Recursive processing** - Process subdirectories
- 🎨 **Quality preservation** - High-quality PNG output
- 📊 **Progress tracking** - Real-time conversion progress
- 🖥️ **Cross-platform** - Works on Windows, macOS, and Linux
- 🗂️ **Organized output** - Optional organized folder structure
- 🔄 **Overwrite protection** - Safe conversion with conflict handling

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Pillow click
```

## Usage

### Basic Usage

Convert all JPG files in current directory:
```bash
python jpg2png.py
```

Convert all JPG files in specific folder:
```bash
python jpg2png.py /path/to/images
```

### Advanced Usage

Convert with custom output folder:
```bash
python jpg2png.py /path/to/images --output /path/to/output
```

Convert recursively (including subdirectories):
```bash
python jpg2png.py /path/to/images --recursive
```

Add timestamp to output filenames:
```bash
python jpg2png.py /path/to/images --timestamp
```

Use GUI folder picker:
```bash
python jpg2png.py --gui
```

### Full Command Options

```bash
python jpg2png.py [FOLDER_PATH] [OPTIONS]

Options:
  -o, --output PATH       Output directory for PNG files
  -r, --recursive         Process subdirectories recursively
  -t, --timestamp         Add timestamp to output filenames
  -g, --gui               Use GUI folder picker
  --overwrite             Overwrite existing PNG files
  --quality INTEGER       PNG compression quality (1-9, default: 6)
  --help                  Show this message and exit
```

## Examples

### Example 1: Simple Conversion
```bash
# Convert all JPG files in current directory
python jpg2png.py

# Convert all JPG files in specific folder
python jpg2png.py ~/Pictures/vacation
```

### Example 2: Organized Output
```bash
# Convert and organize output in separate folder
python jpg2png.py ~/Pictures/vacation --output ~/Pictures/vacation_png

# Convert with timestamp in filenames
python jpg2png.py ~/Pictures/vacation --timestamp
```

### Example 3: Recursive Processing
```bash
# Convert all JPG files in folder and subfolders
python jpg2png.py ~/Pictures --recursive --output ~/Pictures/converted
```

### Example 4: GUI Mode
```bash
# Use GUI to select folder
python jpg2png.py --gui

# GUI with custom output
python jpg2png.py --gui --output ~/Desktop/converted
```

## Output Naming

The tool uses intelligent naming for output files:

- **Standard**: `image.jpg` → `image.png`
- **With timestamp**: `image.jpg` → `image_20240115_143022.png`
- **Conflict handling**: `image.jpg` → `image_1.png`, `image_2.png`, etc.

## Error Handling

The tool handles common scenarios:

- **Invalid images**: Skips corrupted JPG files with warning
- **Permission errors**: Reports access issues
- **Disk space**: Checks available space before conversion
- **Existing files**: Prevents accidental overwrites (unless --overwrite is used)

## Performance

- **Memory efficient**: Processes images one at a time
- **Progress indication**: Shows real-time progress for large batches
- **Speed optimized**: Uses Pillow's optimized PNG encoder

## Troubleshooting

### Common Issues

1. **"No JPG files found"**
   - Ensure the folder contains .jpg or .jpeg files
   - Check file extensions (case-insensitive)

2. **"Permission denied"**
   - Check read/write permissions for source and output folders
   - On macOS/Linux: `chmod +x jpg2png.py`

3. **"Module not found"**
   - Install dependencies: `pip install -r requirements.txt`

4. **"GUI not available"**
   - Install tkinter: Usually included with Python
   - On Ubuntu: `sudo apt-get install python3-tk`

## Development

### Project Structure
```
jpg2png/
├── jpg2png.py          # Main CLI tool
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── examples/          # Example usage
```

### Adding Features

To add new features, modify the `ImageConverter` class in `jpg2png.py`. The tool is designed to be easily extensible.

## License

MIT License - feel free to use and modify as needed.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions, please open an issue on the repository or contact the maintainer.