# Data Visualizer CLI

A simple command-line tool for visualizing CSV data with basic charts.

## Features

- 📊 **Multiple chart types** - Bar charts and line plots
- 🔍 **Auto-detection** - Automatically detects numeric columns
- 🎨 **Customizable** - Specify X and Y axes manually
- 💾 **Save output** - Export charts as PNG files
- 📈 **Quick visualization** - Fast plotting for data analysis

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
pip install pandas matplotlib click
```

## Usage

### Basic Usage

Visualize CSV with automatic column detection:
```bash
python data_visualizer.py data.csv
```

### Advanced Usage

Create bar chart with specific columns:
```bash
python data_visualizer.py data.csv --chart bar --x category --y values
```

Create line plot:
```bash
python data_visualizer.py data.csv --chart line --x date --y sales
```

Save chart to file:
```bash
python data_visualizer.py data.csv --output chart.png
```

### Full Command Options

```bash
python data_visualizer.py CSV_FILE [OPTIONS]

Arguments:
  CSV_FILE  Path to the CSV file

Options:
  --chart [bar|line]       Chart type (default: bar)
  --x TEXT                 X-axis column name
  --y TEXT                 Y-axis column name
  --output PATH            Output file path for saving chart
  --title TEXT             Chart title (default: Data Visualization)
  --help                   Show this message and exit
```

## Examples

### Example 1: Sales Data
```bash
python data_visualizer.py sales.csv --chart line --x month --y revenue --title "Monthly Sales"
```

### Example 2: Category Analysis
```bash
python data_visualizer.py products.csv --x category --y count --output analysis.png
```

## Requirements

- CSV file with at least two numeric columns
- For manual axis specification, column names must match exactly

## Error Handling

- **Missing columns**: Provides clear error messages
- **Invalid data**: Handles non-numeric data gracefully
- **File not found**: Checks file existence before processing

## License

MIT License - feel free to use and modify as needed.