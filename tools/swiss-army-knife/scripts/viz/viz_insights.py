import pandas as pd
import numpy as np
from typing import Dict

def analyze_data(df: pd.DataFrame) -> Dict:
    """Generate statistical insights about the dataset."""
    insights = {
        'summary': {},
        'correlations': {},
        'trends': {},
        'outliers': {}
    }
    
    # Basic statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    insights['summary'] = {
        'rows': len(df),
        'columns': len(df.columns),
        'numeric_columns': numeric_cols.tolist(),
        'categorical_columns': df.select_dtypes(exclude=[np.number]).columns.tolist(),
        'stats': df[numeric_cols].describe().to_dict()
    }
    
    # Correlations
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        strong_corr = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                if abs(corr.iloc[i,j]) > 0.5:
                    strong_corr.append({
                        'columns': (corr.columns[i], corr.columns[j]),
                        'correlation': corr.iloc[i,j]
                    })
        insights['correlations'] = strong_corr
    
    # Trends
    for col in numeric_cols:
        trends = df[col].agg(['mean', 'min', 'max']).to_dict()
        insights['trends'][col] = {
            'direction': 'increasing' if df[col].is_monotonic_increasing else
                        'decreasing' if df[col].is_monotonic_decreasing else 'varying',
            'stats': trends
        }
    
    # Outliers
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))][col]
        if not outliers.empty:
            insights['outliers'][col] = {
                'count': len(outliers),
                'values': outliers.tolist()
            }
    
    return insights