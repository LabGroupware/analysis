import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from create_aggregate import create_aggregate, actions_lists  # あらかじめ同ディレクトリか適切な場所に保存された関数ファイル
from vi import plot_stacked_bar_grids  # あらかじめ同ディレクトリか適切な場所に保存された関数ファイル

base_dir = Path('./saga')
thread_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('thread_')]
actions = ["create_user_profile", "create_file_object", "create_organization", "create_team", "create_task"]

results_processed = []
results_success_client = []
results_success_sever = []
actions_data_sets = {
    "create_user_profile": pd.DataFrame({
        "Key": actions_lists["create_user_profile"],
    }),
    "create_file_object": pd.DataFrame({
        "Key": actions_lists["create_file_object"],
    }),
    "create_organization": pd.DataFrame({
        "Key": actions_lists["create_organization"],
    }),
    "create_team": pd.DataFrame({
        "Key": actions_lists["create_team"],
    }),
    "create_task": pd.DataFrame({
        "Key": actions_lists["create_task"],
    }),
}
last_data = pd.DataFrame({}, index=["create_user_profile", "create_file_object", "create_organization", "create_team", "create_task"])

for t_dir in thread_dirs:
    thread_count = int(t_dir.name.replace('thread_', ''))
    for action in actions:
        action_dir = t_dir / action
        if not action_dir.exists():
            continue

        df_list = []
        for csv_file in action_dir.glob('*.csv'):
            df = pd.read_csv(csv_file)

            df['TotalTime_ms'] = df['TotalTime'].str.replace('ms', '', regex=False).astype(int)
            time_cols = ['StartTime', 'ReceivedDatetime', 'LastActionDatetime', 'ProcessStartDatetime', 'ActionDatetime']
            for col in time_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            df['StartTime'] = pd.to_datetime(df['StartTime'], utc=True)
            df['ActionDatetime'] = pd.to_datetime(df['ActionDatetime'], utc=True)
            df['ReceivedDatetime'] = pd.to_datetime(df['ReceivedDatetime'], utc=True)
            df['LastActionDatetime'] = pd.to_datetime(df['LastActionDatetime'], utc=True)
            df['ProcessStartDatetime'] = pd.to_datetime(df['ProcessStartDatetime'], utc=True)

            success_row = df[df['EventType'] == 'JOB_SUCCESS']
            if not success_row.empty:
                success_process_start_datetime = success_row['ProcessStartDatetime'].iloc[0]
                df['DatetimeDiff_ms'] = (df['LastActionDatetime'] - success_process_start_datetime).dt.total_seconds() * 1000
            else:
                print(f"JOB_SUCCESS not found in {csv_file}")
                # df['DatetimeDiff_ms'] = None
            df_list.append(df)

            # # JOB_SUCCESS のデータが一つであることを前提に取得
            # success_row = data[data['EventType'] == 'JOB_SUCCESS']
            # print(success_row)
            # if not success_row.empty:
            #     success_process_start_datetime = success_row['ProcessStartDatetime'].iloc[0]

            #     # JOB_PROCESSED の LastActionDatetime と JOB_SUCCESS の ProcessStartDatetime の差を計算
            #     processed['DatetimeDiff_ms'] = (processed['LastActionDatetime'] - success_process_start_datetime).dt.total_seconds() * 1000

            #     # LastActionCode ごとに平均を計算
            #     datetime_diff_stats = processed.groupby('LastActionCode').agg(
            #         DatetimeDiff_mean=('DatetimeDiff_ms', 'mean'),
            #         DatetimeDiff_count=('DatetimeDiff_ms', 'count'),
            #     )
            # else:
            #     # JOB_SUCCESS が存在しない場合は空の DataFrame を返す
            #     datetime_diff_stats = pd.DataFrame()

        if not df_list:
            continue

        data = pd.concat(df_list, ignore_index=True)
        record_count = len(data)  # action+threadごとの総データ件数

        processed_stats, success_client_stats, success_sever_stats, action_set, last_action_time_diff = create_aggregate(data, action)

        actions_data_sets[action][thread_count] = action_set
        last_data.loc[action, thread_count] = last_action_time_diff
        # target_df = target_df.merge(pd.DataFrame({f"thread_{thread_count}": action_set}), left_index=True, right_index=True, how='outer')
        # target_df[f"thread_{thread_count}"] = action_set
        
        # print(f"Thread: {thread_count}, Action: {action}, Record count: {record_count}")
        # print(diff_stats)

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
processed_all.to_csv('saga/res/aggregate/processed_all.csv', index=False)
success_client_all.to_csv('saga/res/aggregate/success_client_all.csv', index=False)
success_server_all.to_csv('saga/res/aggregate/success_server_all.csv', index=False)

print("Complete creating CSV files.", processed_all.shape, success_client_all.shape, success_server_all.shape)

data_sets = [
    (actions_data_sets["create_user_profile"], "Create User Profile"),
    (actions_data_sets["create_file_object"], "Create File Object"),
    (actions_data_sets["create_organization"], "Create Organization"),
    (actions_data_sets["create_team"], "Create Team"),
    (actions_data_sets["create_task"], "Create Task")
]

plot_stacked_bar_grids(data_sets, last_data, n_cols=3, figsize=(4.5, 3.5))