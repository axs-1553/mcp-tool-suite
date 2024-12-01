import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Tuple, Optional

def create_interactive_plot(df: pd.DataFrame, plot_type: str, x: str, y: Optional[str] = None,
                          hue: Optional[str] = None, title: Optional[str] = None,
                          kind: Optional[str] = None, stacked: bool = False) -> go.Figure:
    if plot_type == 'line':
        fig = px.line(df, x=x, y=y, color=hue, title=title, markers=True)
    elif plot_type == 'bar':
        fig = px.bar(df, x=x, y=y, color=hue, title=title, barmode='stack' if stacked else 'group')
    elif plot_type == 'scatter':
        fig = px.scatter(df, x=x, y=y, color=hue, size=hue if kind == 'bubble' else None,
                        title=title, hover_data=df.columns)
    elif plot_type == 'box':
        fig = px.box(df, x=x, y=y, color=hue, title=title)
    elif plot_type == 'violin':
        fig = px.violin(df, x=x, y=y, color=hue, title=title, box=True)
    elif plot_type == 'heatmap':
        if y:
            pivot = df.pivot_table(values=y, index=x, columns=hue or 'value')
            fig = px.imshow(pivot, title=title, aspect='auto')
        else:
            correlation = df.corr()
            fig = px.imshow(correlation, title=title)
    elif plot_type == 'pie':
        fig = px.pie(df, values=y, names=x, title=title)
    else:
        raise ValueError(f"Interactive plot type {plot_type} not supported")
    
    fig.update_layout(
        title_x=0.5,
        margin=dict(t=100),
        showlegend=True,
        template='plotly_white'
    )
    return fig

def create_interactive_subplots(df: pd.DataFrame, subplots: List[Tuple[str, dict]], 
                              layout: Tuple[int, int]) -> go.Figure:
    rows, cols = layout
    fig = make_subplots(rows=rows, cols=cols, subplot_titles=[p[1].get('title', '') for p in subplots])
    
    for i, (plot_type, params) in enumerate(subplots, 1):
        row = (i - 1) // cols + 1
        col = (i - 1) % cols + 1
        
        subplot = create_interactive_plot(df, plot_type, 
                                       x=params.get('x'),
                                       y=params.get('y'),
                                       hue=params.get('hue'),
                                       kind=params.get('kind'),
                                       stacked=params.get('stacked', False))
        
        for trace in subplot.data:
            fig.add_trace(trace, row=row, col=col)
    
    fig.update_layout(height=400*rows, showlegend=True, template='plotly_white')
    return fig