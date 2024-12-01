import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Tuple, Optional

def create_subplot(fig: plt.Figure, subplot_spec: str, df: pd.DataFrame, 
                  plot_type: str, x: str, y: Optional[str] = None, 
                  hue: Optional[str] = None, title: Optional[str] = None,
                  kind: Optional[str] = None, stacked: bool = False,
                  palette: Optional[str] = None) -> None:
    ax = fig.add_subplot(subplot_spec)
    
    if palette:
        sns.set_palette(palette)
    
    if plot_type == 'line':
        sns.lineplot(data=df, x=x, y=y, hue=hue, marker='o', ax=ax)
        ax.grid(True)
    elif plot_type == 'bar':
        if stacked and hue:
            df_pivot = df.pivot(index=x, columns=hue, values=y)
            df_pivot.plot(kind='bar', stacked=True, ax=ax)
        else:
            sns.barplot(data=df, x=x, y=y, hue=hue, ax=ax)
    elif plot_type == 'scatter':
        sns.scatterplot(data=df, x=x, y=y, hue=hue, 
                       size=hue if kind == 'bubble' else None, ax=ax)
        ax.grid(True)
    elif plot_type == 'box':
        sns.boxplot(data=df, x=x, y=y, hue=hue, ax=ax)
    elif plot_type == 'violin':
        sns.violinplot(data=df, x=x, y=y, hue=hue, ax=ax)
    elif plot_type == 'heatmap':
        if y:
            pivot = df.pivot_table(values=y, index=x, columns=hue or 'value')
            sns.heatmap(pivot, annot=True, cmap=palette or 'YlOrRd', fmt='.0f', ax=ax)
        else:
            correlation = df.corr()
            sns.heatmap(correlation, annot=True, cmap=palette or 'YlOrRd', fmt='.2f', ax=ax)
    elif plot_type == 'pie':
        ax.pie(df[y], labels=df[x], autopct='%1.1f%%')
        ax.axis('equal')
    elif plot_type == 'area':
        if stacked and hue:
            df_pivot = df.pivot(index=x, columns=hue, values=y)
            df_pivot.plot(kind='area', stacked=True, ax=ax)
        else:
            df.plot(kind='area', x=x, y=y, ax=ax)
        ax.grid(True)
    elif plot_type == 'radar':
        ax = plt.subplot(subplot_spec, projection='polar')
        categories = df[x].tolist()
        values = df[y].tolist()
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
        values = np.concatenate((values, [values[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        categories = np.concatenate((categories, [categories[0]]))
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories[:-1])
    elif plot_type == 'donut':
        ax.pie(df[y], labels=df[x], autopct='%1.1f%%')
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        ax.axis('equal')
    
    if title:
        ax.set_title(title)

def create_multi_plot(df: pd.DataFrame, subplots: List[Tuple[str, dict]], 
                     layout: Tuple[int, int], figsize: tuple = (10, 6),
                     palette: Optional[str] = None) -> plt.Figure:
    rows, cols = layout
    fig = plt.figure(figsize=figsize)
    
    for i, (plot_type, params) in enumerate(subplots, 1):
        create_subplot(fig, f"{rows}{cols}{i}", df, plot_type, 
                      x=params.get('x'), 
                      y=params.get('y'),
                      hue=params.get('hue'),
                      title=params.get('title'),
                      kind=params.get('kind'),
                      stacked=params.get('stacked', False),
                      palette=palette)
    
    plt.tight_layout()
    return fig