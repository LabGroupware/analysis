import pandas as pd
from pathlib import Path
from create_aggregate import create_aggregate  # あらかじめ同ディレクトリか適切な場所に保存された関数ファイル

base_dir = Path('./datasets/wait_saga')
thread_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('thread_')]
actions = ["create_user_profile", "create_file_object", "create_organization", "create_team", "create_task"]

results_processed = []
results_success_client = []
results_success_sever = []

for t_dir in thread_dirs:
    thread_count = int(t_dir.name.replace('thread_', ''))
    for action in actions:
        action_dir = t_dir / action
        if not action_dir.exists():
            continue

        df_list = []
        for csv_file in action_dir.glob('*.csv'):
            df_list.append(pd.read_csv(csv_file))
        if not df_list:
            continue

        data = pd.concat(df_list, ignore_index=True)
        record_count = len(data)  # action+threadごとの総データ件数

        processed_stats, success_client_stats, success_sever_stats = create_aggregate(data)

        # processed_statsはLastActionCodeごとの集計結果
        if not processed_stats.empty:
            p_stats = processed_stats.copy()
            p_stats['thread'] = thread_count
            p_stats['action'] = action
            p_stats['record_count'] = record_count
            p_stats.reset_index(inplace=True)  # LastActionCodeを列へ
            results_processed.append(p_stats)

        # success_statsは1行の集計結果
        if not success_client_stats.empty:
            s_stats = success_client_stats.copy()
            s_stats['thread'] = thread_count
            s_stats['action'] = action
            s_stats['record_count'] = record_count
            results_success_client.append(s_stats)

        if not success_sever_stats.empty:
            s_stats = success_sever_stats.copy()
            s_stats['thread'] = thread_count
            s_stats['action'] = action
            s_stats['record_count'] = record_count
            results_success_sever.append(s_stats)

processed_all = pd.concat(results_processed, ignore_index=True) if results_processed else pd.DataFrame()
success_client_all = pd.concat(results_success_client, ignore_index=True) if results_success_client else pd.DataFrame()
success_server_all = pd.concat(results_success_sever, ignore_index=True) if results_success_sever else pd.DataFrame()

# CSV出力
processed_all.to_csv('aggregate/processed_all.csv', index=False)
success_client_all.to_csv('aggregate/success_client_all.csv', index=False)
success_server_all.to_csv('aggregate/success_server_all.csv', index=False)

print("Complete creating CSV files.", processed_all.shape, success_client_all.shape, success_server_all.shape)