# Song Manager

A simple command-line application for managing and singing songs from text files.

## Features

- 🎵 **Song library** - Load songs from configuration file
- 🎤 **Interactive singing** - Display song lyrics
- 🔄 **Random selection** - Choose random song
- 📋 **Song list** - View available songs
- 🛡️ **Error handling** - Robust file and input handling

## Installation

### Prerequisites

- Python 3.7 or higher

### No Dependencies

This project uses only Python standard library modules.

## Usage

### Basic Usage

Run the song manager:
```bash
python main.py
```

### Configuration

Songs are configured in `Config.ini`:

```ini
[songs]
HappyBirthday = songs/HappyBirthday.txt
TwinkleTwinkle = songs/TwinkleTwinkle.txt
```

## File Structure

```
song_manager/
├── main.py              # Main application
├── song_manager.py      # Song management functions
├── Config.ini          # Song configuration
├── songs/              # Song lyrics folder
│   ├── HappyBirthday.txt
│   ├── TwinkleTwinkle.txt
│   └── ...
└── Test.py             # Test file
```

## Example Songs

The `songs/` folder contains sample song lyrics files. Each file should contain the lyrics as plain text.

Example `HappyBirthday.txt`:
```
Happy Birthday to you
Happy Birthday to you
Happy Birthday dear friend
Happy Birthday to you!
```

## Features Overview

- **Load songs**: Reads song paths from `Config.ini`
- **Display menu**: Shows numbered list of available songs
- **Random selection**: Option to choose random song
- **Error handling**: Graceful handling of missing files
- **Loop functionality**: Continue singing or exit

## License

MIT License - feel free to use and modify as needed.