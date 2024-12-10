import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def create_aggregate(data: pd.DataFrame):
    # # TotalTimeの"ms"を除去して整数化
    data['TotalTime_ms'] = data['TotalTime'].str.replace('ms', '', regex=False).astype(int)

    # 日付をdatetime型へ変換（UTCを仮定、タイムゾーンは任意）
    # ISO8601はpandasが自動認識しますが、必要なら utc=True オプションを付与
    time_cols = ['StartTime', 'ReceivedDatetime', 'LastActionDatetime', 'ProcessStartDatetime', 'ActionDatetime']
    for col in time_cols:
        # 欠損値対策として errors='coerce'。必ず日付がある前提でなければエラー回避にも有効
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors='coerce')

    data['StartTime'] = pd.to_datetime(data['StartTime'], utc=True)
    data['ActionDatetime'] = pd.to_datetime(data['ActionDatetime'], utc=True)
    data['ReceivedDatetime'] = pd.to_datetime(data['ReceivedDatetime'], utc=True)
    data['LastActionDatetime'] = pd.to_datetime(data['LastActionDatetime'], utc=True)
    data['ProcessStartDatetime'] = pd.to_datetime(data['ProcessStartDatetime'], utc=True)

    # JOB_PROCESSEDの解析
    processed = data[data['EventType'] == 'JOB_PROCESSED'].copy()

    # LastActionCodeごとに集計: TotalTime_ms と ActionMinusStart_ms
    processed_stats = processed.groupby('LastActionCode').agg(
        TotalTime_count=('TotalTime_ms', 'count'),
        TotalTime_mean=('TotalTime_ms', 'mean'),
        TotalTime_max=('TotalTime_ms', 'max'),
        TotalTime_min=('TotalTime_ms', 'min'),
        TotalTime_median=('TotalTime_ms', 'median'),
        TotalTime_var=('TotalTime_ms', 'var'),
    )

    # JOB_SUCCESSの解析
    success = data[data['EventType'] == 'JOB_SUCCESS'].copy()


    # Successの場合: TotalTime_msと(ActionDatetime - ProcessStartDatetime)
    success['SeverTotalTime_ms'] = (success['ActionDatetime'] - success['ProcessStartDatetime']).dt.total_seconds() * 1000

    # JOB_SUCCESSは必ず1レコード/ジョブとあるが、複数ジョブ分の集計を想定し、全SUCCESSの統計を取る
    success_stats = success.agg(
        ClientTotalTime_count=('TotalTime_ms', 'count'),
        ClientTotalTime_mean=('TotalTime_ms', 'mean'),
        ClientTotalTime_max=('TotalTime_ms', 'max'),
        ClientTotalTime_min=('TotalTime_ms', 'min'),
        ClientTotalTime_median=('TotalTime_ms', 'median'),
        ClientTotalTime_var=('TotalTime_ms', 'var'),

        SeverTotalTime_count=('SeverTotalTime_ms', 'count'),
        SeverTotalTime_mean=('SeverTotalTime_ms', 'mean'),
        SeverTotalTime_max=('SeverTotalTime_ms', 'max'),
        SeverTotalTime_min=('SeverTotalTime_ms', 'min'),
        SeverTotalTime_median=('SeverTotalTime_ms', 'median'),
        SeverTotalTime_var=('SeverTotalTime_ms', 'var')
    )

    return processed_stats, success_stats

base_dir = Path('./datasets/wait_saga')  # データのあるディレクトリ
thread_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('thread_')]

# アクション名の一覧(必要なら自動取得も可能)
actions = ["create_user_profile", "create_file_object", "create_organization", "create_team", "create_task"]

results_processed = []
results_success = []

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
        record_count = len(data)
        processed_stats, success_stats = create_aggregate(data)

        # processed_statsはLastActionCode毎
        if not processed_stats.empty:
            p_stats = processed_stats.copy()
            p_stats['thread'] = thread_count
            p_stats['action'] = action
            p_stats['record_count'] = record_count
            p_stats.reset_index(inplace=True)  # LastActionCodeを列に戻す
            results_processed.append(p_stats)

        # success_statsは1行のみ
        s_stats = success_stats.copy()
        s_stats['thread'] = thread_count
        s_stats['action'] = action
        s_stats['record_count'] = record_count
        results_success.append(s_stats)

# 全結果を結合
processed_all = pd.concat(results_processed, ignore_index=True) if results_processed else pd.DataFrame()
success_all = pd.concat(results_success, ignore_index=True) if results_success else pd.DataFrame()

# 結果を表示
print("=== PROCESSED Stats (例) ===")
print(processed_all.all())

print("=== SUCCESS Stats (例) ===")
print(success_all.all())

# 可視化例（JOB_SUCCESSのClientTotalTime_meanをスレッド数ごとにプロット）
plt.figure(figsize=(10,6))
for action in actions:
    subset = success_all[success_all['action'] == action]
    print(subset)
    # if not subset.empty:
    #     plt.plot(subset['thread'], subset['ClientTotalTime_mean'], marker='o', label=action)

plt.xlabel('Thread Count')
plt.ylabel('Average ClientTotalTime (ms)')
plt.title('Average ClientTotalTime by Thread Count and Action (JOB_SUCCESS)')
plt.legend()
plt.tight_layout()
plt.show()