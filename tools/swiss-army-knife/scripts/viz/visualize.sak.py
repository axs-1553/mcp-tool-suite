import argparse
import json
from pathlib import Path
import pandas as pd
from typing import List, Tuple
import matplotlib.pyplot as plt

try:
    import viz_insights
    import viz_static
    import viz_interactive
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False

def load_data(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if path.suffix == '.csv':
        return pd.read_csv(path)
    elif path.suffix == '.json':
        return pd.read_json(path)
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")

def parse_subplots(subplot_str: str) -> List[Tuple[str, dict]]:
    subplots = []
    for plot_config in subplot_str.split('|'):
        parts = plot_config.split(';')
        plot_type = parts[0]
        params = {}
        for param in parts[1:]:
            key, value = param.split('=')
            params[key] = value
        subplots.append((plot_type, params))
    return subplots

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true', help='Show script information')
    parser.add_argument('input', nargs='?', help='Input data file')
    parser.add_argument('output', nargs='?', help='Output image file')
    parser.add_argument('--type', help='Type of plot')
    parser.add_argument('--x', help='X-axis column')
    parser.add_argument('--y', help='Y-axis column')
    parser.add_argument('--hue', help='Column for color grouping')
    parser.add_argument('--title', help='Plot title')
    parser.add_argument('--figsize', help='Figure size (width,height)')
    parser.add_argument('--kind', help='Subtype of plot')
    parser.add_argument('--stacked', action='store_true', help='Create stacked charts')
    parser.add_argument('--palette', help='Color palette name')
    parser.add_argument('--subplots', help='Subplot configuration')
    parser.add_argument('--layout', help='Subplot layout (rows,cols)')
    parser.add_argument('--insights', action='store_true', help='Generate data insights')
    parser.add_argument('--interactive', action='store_true', help='Create interactive HTML plot')
    
    args = parser.parse_args()
    
    if args.info:
        print("""
        Tool Name: Enhanced Data Visualizer
        Description: Create visualizations from data files
        
        Plot Types: line, bar, scatter, box, violin, heatmap, pie, area, radar, donut
        
        Features:
        - Multiple subplots with --subplots and --layout
        - Custom color palettes with --palette
        - Stacked charts with --stacked
        - Data insights with --insights
        - Interactive plots with --interactive
        
        Examples:
          swiss-army-knife visualize data.csv viz --interactive --insights \\
            --subplots "scatter;x=x;y=y|bar;x=category;y=value"
        """)
        return

    if not args.input or not args.output or not MODULES_AVAILABLE:
        parser.print_help()
        return

    df = load_data(args.input)
    
    if args.insights:
        insights = viz_insights.analyze_data(df)
        insight_file = Path(args.output).with_suffix('.insights.json')
        with open(insight_file, 'w') as f:
            json.dump(insights, f, indent=2)
        print(f"Generated insights: {insight_file}")
    
    if args.interactive:
        output_html = Path(args.output).with_suffix('.html')
        
        if args.subplots:
            subplots = parse_subplots(args.subplots)
            layout = tuple(map(int, args.layout.split(','))) if args.layout else (len(subplots), 1)
            fig = viz_interactive.create_interactive_subplots(df, subplots, layout)
        else:
            fig = viz_interactive.create_interactive_plot(df, args.type, args.x, args.y, args.hue, 
                                                       args.title, args.kind, args.stacked)
        
        fig.write_html(output_html)
        print(f"Created interactive visualization: {output_html}")
    else:
        figsize = (10, 6)
        if args.figsize:
            width, height = map(float, args.figsize.split(','))
            figsize = (width, height)

        if args.subplots:
            subplots = parse_subplots(args.subplots)
            layout = tuple(map(int, args.layout.split(','))) if args.layout else (len(subplots), 1)
            fig = viz_static.create_multi_plot(df, subplots, layout, figsize, args.palette)
        else:
            fig = plt.figure(figsize=figsize)
            viz_static.create_subplot(fig, '111', df, args.type, args.x, args.y, args.hue, 
                                    args.title, args.kind, args.stacked, args.palette)
        
        plt.savefig(args.output, bbox_inches='tight', dpi=300)
        print(f"Created visualization: {args.output}")

if __name__ == '__main__':
    main()