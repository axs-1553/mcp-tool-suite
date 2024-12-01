# Data Visualization Tools

A comprehensive suite of data visualization tools for the Swiss Army Knife MCP server.

## Installation
```bash
pip install -r requirements.txt
```

## Components

### visualize.sak.py
Main script that handles all visualization operations.

#### Features
- Multiple plot types: line, bar, scatter, box, violin, heatmap, pie, area, radar, donut
- Static and interactive outputs
- Data insights generation
- Multiple subplot support
- Custom color palettes
- Stacked chart options

#### Usage
```bash
swiss-army-knife visualize input_data.csv output.png --type bar --x category --y value
```

#### Common Commands
```bash
# Get help and options
swiss-army-knife visualize --info

# Create an interactive plot
swiss-army-knife visualize data.csv plot.html --interactive --type scatter --x x_col --y y_col

# Generate data insights
swiss-army-knife visualize data.csv stats --insights

# Create multiple subplots
swiss-army-knife visualize data.csv multiplot.png --subplots "scatter;x=x;y=y|bar;x=cat;y=val" --layout "2,1"
```

### Support Modules

#### viz_interactive.py
Handles interactive plot creation using Plotly.
- Interactive plots with hover data
- Dynamic subplot layouts
- Export to HTML format

#### viz_static.py
Creates static plots using Matplotlib and Seaborn.
- High-quality static images
- Multiple plot types
- Custom color palettes
- Advanced layout control

#### viz_insights.py
Generates statistical insights about datasets.
- Basic statistics
- Correlation analysis
- Trend detection
- Outlier identification

## Input Data Format
- Supports CSV and JSON files
- Data should be in tabular format
- Column names required for x/y axis specification

## Examples

### Basic Line Plot
```bash
swiss-army-knife visualize data.csv line_plot.png --type line --x date --y value --title "Time Series"
```

### Interactive Scatter Plot with Color Groups
```bash
swiss-army-knife visualize data.csv scatter.html --interactive --type scatter --x x --y y --hue category
```

### Multiple Subplots with Different Types
```bash
swiss-army-knife visualize data.csv combo.png --subplots "scatter;x=x;y=y|bar;x=category;y=value|line;x=date;y=trend" --layout "3,1"
```

### Data Insights with Visualization
```bash
swiss-army-knife visualize data.csv analysis --insights --type heatmap
```

## Tips
1. Use `--interactive` for exploratory data analysis
2. Generate insights first to understand your data
3. Experiment with different color palettes using `--palette`
4. Use quotes for subplot configurations
5. Check subplot layout matches your configuration