import pandas as pd

def create_aggregate(data: pd.DataFrame):
    # ResponseTimeの統計量を計算
    processed_stats = data['ResponseTime_ms'].agg(['count', 'mean', 'median', 'max', 'min', 'var']).rename({
        'count': 'Count',
        'mean': 'Mean',
        'median': 'Median',
        'max': 'Max',
        'min': 'Min',
        'var': 'Variance'
    })
    
    # StatusCodeのカウントを計算
    statuscode_counts = data['StatusCode'].value_counts().reset_index().rename(columns={
        'index': 'StatusCode',
        'StatusCode': 'Count'
    })
    
    return processed_stats, statuscode_counts