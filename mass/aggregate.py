import pandas as pd
from pathlib import Path
from create_aggregate import create_aggregate
from vi import visualize_results, display_results

base_dir = Path('./mass')
thread_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('thread_')]
scenarios = [
    "create_user_profile",
    "create_organization",
    "create_task",
    "get_users",
    "get_organizations",
    "get_organizations_with_users",
    # "sc1", "sc2", "sc3", "sc4", "sc5", "sc6", "sc7", "sc8", "sc9", "sc10",
    # "sc11", "sc12", "sc13", "sc14", "sc15", "sc16", "sc17", "sc18", "sc19", "sc20",
    # "sc21", "sc22", "sc23", "sc24", "sc25", "sc26", "sc27"
]

aggregate_results = []
threads = []
for t_dir in thread_dirs:
    thread_count = int(t_dir.name.replace('thread_', ''))
    threads.append(thread_count)
    for scenario in scenarios:
        scenario_dir = t_dir / scenario
        if not scenario_dir.exists():
            continue

        df_list = []
        for csv_file in Path(scenario_dir).rglob("*.csv"):
            df = pd.read_csv(csv_file)

            df['ResponseTime_ms'] = df['ResponseTime'].astype(int)

            q = df['ResponseTime_ms'].quantile(0.85)

            df = df[df['ResponseTime_ms'] < q]

            time_cols = ['SendDatetime', 'ReceivedDatetime']
            for col in time_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], utc=True, errors='coerce')
            df['SendDatetime'] = pd.to_datetime(df['SendDatetime'], utc=True)
            df['ReceivedDatetime'] = pd.to_datetime(df['ReceivedDatetime'], utc=True)
            df_list.append(df)

        if not df_list:
            continue

        data = pd.concat(df_list, ignore_index=True)
        record_count = len(data)  # scenario+threadごとの総データ件数

        processed_stats, statuscode_counts = create_aggregate(data)
            
        # 結果を辞書にまとめる
        result = {
            'Thread': thread_count,
            'Scenario': scenario,
            'RecordCount': record_count,
            'ResponseTime_Count': processed_stats['Count'],
            'ResponseTime_Mean': processed_stats['Mean'],
            'ResponseTime_Median': processed_stats['Median'],
            'ResponseTime_Max': processed_stats['Max'],
            'ResponseTime_Min': processed_stats['Min'],
            'ResponseTime_Variance': processed_stats['Variance'],
            'StatusCode_Counts': statuscode_counts.to_dict(orient='records')
        }
        
        aggregate_results.append(result)
    
# 結果を表示
display_results(aggregate_results)

# 結果を可視化
visualize_results(aggregate_results, scenarios, threads)