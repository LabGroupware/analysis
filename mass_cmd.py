import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import argparse

def create_aggregate(data: pd.DataFrame):
    """
    与えられたDataFrameに対してResponseTimeとStatusCodeの集計を行います。
    
    Parameters:
        data (pd.DataFrame): 入力データ
    
    Returns:
        processed_stats (pd.DataFrame): ResponseTimeの統計値
        statuscode_counts (pd.DataFrame): StatusCodeのカウント
    """
    # TotalTimeを整数に変換
    data['ResponseTime_ms'] = data['ResponseTime'].astype(int)
    
    # タイムスタンプをdatetime型に変換（UTCを仮定）
    time_cols = ['SendDatetime', 'ReceivedDatetime']
    for col in time_cols:
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], utc=True, errors='coerce')
    
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

def aggregate_data(base_dir: Path, threads, actions):
    """
    ディレクトリ構造に基づいてデータを集計します。
    
    Parameters:
        base_dir (Path): データが格納されている基点ディレクトリ
        threads (list): スレッド数のリスト
        actions (list): アクション名のリスト
    
    Returns:
        aggregate_results (list): 集計結果のリスト
    """
    aggregate_results = []
    
    for thread in threads:
        for action in actions:
            csv_dir = base_dir / f"thread_{thread}" / action / "batch"
            if not csv_dir.exists() or not csv_dir.is_dir():
                print(f"ディレクトリが存在しません: {csv_dir}")
                continue
            
            csv_files = list(csv_dir.glob('*.csv'))
            if not csv_files:
                print(f"CSVファイルが見つかりません: {csv_dir}")
                continue
            
            # 全CSVを読み込む
            df_list = []
            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    df_list.append(df)
                except Exception as e:
                    print(f"CSVの読み込みに失敗しました: {csv_file}. エラー: {e}")
                    continue
            
            if not df_list:
                print(f"有効なCSVファイルがありません: {csv_dir}")
                continue
            
            data = pd.concat(df_list, ignore_index=True)
            
            # データ件数
            record_count = len(data)
            
            # 集計処理
            processed_stats, statuscode_counts = create_aggregate(data)
            
            # 結果を辞書にまとめる
            result = {
                'Thread': thread,
                'Action': action,
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
    
    return aggregate_results

def display_results(aggregate_results):
    """
    集計結果を表示します。
    
    Parameters:
        aggregate_results (list): 集計結果のリスト
    """
    # ResponseTimeの統計を表示
    response_time_data = []
    for result in aggregate_results:
        response_time_data.append({
            'Thread': result['Thread'],
            'Action': result['Action'],
            'RecordCount': result['RecordCount'],
            'Count': result['ResponseTime_Count'],
            'Mean': result['ResponseTime_Mean'],
            'Median': result['ResponseTime_Median'],
            'Max': result['ResponseTime_Max'],
            'Min': result['ResponseTime_Min'],
            'Variance': result['ResponseTime_Variance']
        })
    
    df_response = pd.DataFrame(response_time_data)
    print("\n=== ResponseTimeの統計 ===")
    print(df_response.to_markdown(index=False))
    
    # StatusCodeのカウントを表示
    print("\n=== StatusCodeのカウント ===")
    for result in aggregate_results:
        print(f"\nThread: {result['Thread']}, Action: {result['Action']}, RecordCount: {result['RecordCount']}")
        df_status = pd.DataFrame(result['StatusCode_Counts'])
        print(df_status.to_markdown(index=False))

def visualize_results(aggregate_results, actions, threads):
    """
    集計結果を可視化します。
    
    Parameters:
        aggregate_results (list): 集計結果のリスト
        actions (list): アクション名のリスト
        threads (list): スレッド数のリスト
    """
    # ResponseTimeの平均をアクションごとにプロット
    plt.figure(figsize=(12, 8))
    
    for action in actions:
        mean_values = []
        thread_labels = []
        for thread in threads:
            # 該当するアクションとスレッドのデータを取得
            filtered = [res for res in aggregate_results if res['Action'] == action and res['Thread'] == thread]
            if filtered:
                mean = filtered[0]['ResponseTime_Mean']
                mean_values.append(mean)
                thread_labels.append(thread)
        
        plt.plot(thread_labels, mean_values, marker='o', label=action)
    
    plt.xlabel('Thread Count')
    plt.ylabel('Average ResponseTime (ms)')
    plt.title('Average ResponseTime by Thread Count and Action')
    plt.legend()
    plt.grid(True)
    plt.xticks(threads)
    plt.tight_layout()
    plt.show()
    
    # StatusCodeのカウントをアクションごとに棒グラフで表示
    for action in actions:
        status_counts = {}
        for thread in threads:
            filtered = [res for res in aggregate_results if res['Action'] == action and res['Thread'] == thread]
            if filtered:
                for status in filtered[0]['StatusCode_Counts']:
                    code = status['StatusCode']
                    count = status['Count']
                    if code in status_counts:
                        status_counts[code].append(count)
                    else:
                        status_counts[code] = [count]
        
        # 各StatusCodeごとにプロット
        status_codes = list(status_counts.keys())
        indices = range(len(threads))
        bar_width = 0.15
        plt.figure(figsize=(12, 8))
        
        for i, code in enumerate(status_codes):
            counts = status_counts[code]
            plt.bar([x + bar_width*i for x in indices], counts, bar_width, label=f'StatusCode {code}')
        
        plt.xlabel('Thread Count')
        plt.ylabel('StatusCode Count')
        plt.title(f'StatusCode Counts by Thread Count for Action: {action}')
        plt.xticks([x + bar_width*(len(status_codes)/2) for x in indices], threads)
        plt.legend()
        plt.tight_layout()
        plt.show()

def main():
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="CSVファイルのResponseTimeとStatusCodeを集計・可視化します。")
    parser.add_argument('base_directory', type=str, help='データが格納されている基点ディレクトリのパス')
    args = parser.parse_args()
    
    base_dir = Path(args.base_directory).resolve()
    
    # スレッド数とアクション名の定義
    threads = [10, 50, 100]
    actions = ["create_user_profile", "create_file_object", "create_organization"]
    
    # データの集計
    aggregate_results = aggregate_data(base_dir, threads, actions)
    
    if not aggregate_results:
        print("集計結果がありません。データを確認してください。")
        return
    
    # 結果の表示
    display_results(aggregate_results)
    
    # 結果の可視化
    visualize_results(aggregate_results, actions, threads)

if __name__ == "__main__":
    main()
