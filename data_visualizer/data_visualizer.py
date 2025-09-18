#!/usr/bin/env python3
"""
Simple Data Visualizer CLI

A command-line tool for visualizing CSV data with basic charts.
Supports bar charts and line plots with automatic column detection.

Usage examples:
    python data_visualizer.py data.csv
    python data_visualizer.py data.csv --chart bar --x column1 --y column2 --output chart.png
"""

import pandas as pd
import matplotlib.pyplot as plt
import click
import sys
from pathlib import Path


@click.command()
@click.argument('csv_file', type=click.Path(exists=True))
@click.option('--chart', default='bar', type=click.Choice(['bar', 'line']), help='Chart type: bar or line')
@click.option('--x', help='X-axis column name (optional, uses first numeric if not specified)')
@click.option('--y', help='Y-axis column name (optional, uses second numeric if not specified)')
@click.option('--output', default=None, type=click.Path(), help='Output file path for saving chart (e.g., chart.png)')
@click.option('--title', default='Data Visualization', help='Chart title')
def visualize_csv(csv_file, chart, x, y, output, title):
    """Visualize CSV data with basic charts."""
    try:
        # Load CSV file
        df = pd.read_csv(csv_file)
        print(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
        print(f"Columns: {list(df.columns)}")

        # Auto-detect numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        if len(numeric_cols) < 2 and (x is None or y is None):
            print("Error: Need at least 2 numeric columns for plotting, or specify --x and --y")
            return

        # Set default x and y if not specified
        if x is None:
            x = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[0]
        if y is None and len(numeric_cols) > 1:
            y = numeric_cols[1]
        elif y is None:
            print("Error: Y column must be specified or auto-detected from numeric columns")
            return

        print(f"Plotting {chart} chart: X={x}, Y={y}")

        # Create the plot
        plt.figure(figsize=(10, 6))

        if chart == 'bar':
            plt.bar(df[x], df[y])
            plt.xlabel(x)
            plt.ylabel(y)
        elif chart == 'line':
            plt.plot(df[x], df[y], marker='o')
            plt.xlabel(x)
            plt.ylabel(y)

        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save or show
        if output:
            plt.savefig(output, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {output}")
        else:
            plt.show()

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    visualize_csv()</content>
</xai:function_call name="write_file">
<parameter name="file_path">data_visualizer.py