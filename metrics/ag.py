import pandas as pd
from pathlib import Path
import argparse

def create_aggregate_batch(data: pd.DataFrame):
    """
    BatchデータのResponseTimeとStatusCodeを集計する関数。

    Parameters:
        data (pd.DataFrame): Batch CSVデータ

    Returns:
        batch_stats (pd.Series): ResponseTimeの統計値
        statuscode_counts (pd.DataFrame): StatusCodeのカウント
    """
    # ResponseTimeを数値型に変換
    data['ResponseTime_ms'] = pd.to_numeric(data['ResponseTime'], errors='coerce')
    
    # タイムスタンプをdatetime型に変換（必要なら）
    data['SendDatetime'] = pd.to_datetime(data['SendDatetime'], utc=True, errors='coerce')
    data['ReceivedDatetime'] = pd.to_datetime(data['ReceivedDatetime'], utc=True, errors='coerce')
    
    # ResponseTimeの統計量を計算
    batch_stats = data['ResponseTime_ms'].agg(['count', 'mean', 'median', 'max', 'min', 'var']).rename({
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
    
    return batch_stats, statuscode_counts

def create_aggregate_metrics(memory_data: pd.DataFrame, cpu_data: pd.DataFrame):
    """
    MetricsデータのCPUとMemory使用量を集計する関数。

    Parameters:
        memory_data (pd.DataFrame): Memory Metrics CSVデータ
        cpu_data (pd.DataFrame): CPU Metrics CSVデータ

    Returns:
        memory_stats (pd.DataFrame): NamespaceごとのMemory使用量の統計
        cpu_stats (pd.DataFrame): NamespaceごとのCPU使用量の統計
    """

    # Memory使用量の統計を計算
    memory_columns = ['MemoryUsage', 'AuthMemoryUsage', 'WebsocketMemoryUsage', 'WebGatewayMemoryUsage',
                      'JobMemoryUsage', 'UserProfileMemoryUsage', 'UserPreferenceMemoryUsage',
                      'OrganizationMemoryUsage', 'TeamMemoryUsage', 'PlanMemoryUsage', 'StorageMemoryUsage']
    
    memory_stats = memory_data[memory_columns].agg(['mean', 'median', 'max', 'min', 'var']).transpose().reset_index().rename(columns={'index': 'Namespace'})
    
    # CPU使用量の統計を計算
    cpu_columns = ['CPUUsage', 'AuthCPUUsage', 'WebsocketCPUUsage', 'WebGatewayCPUUsage',
                  'JobCPUUsage', 'UserProfileCPUUsage', 'UserPreferenceCPUUsage',
                  'OrganizationCPUUsage', 'TeamCPUUsage', 'PlanCPUUsage', 'StorageCPUUsage']
    
    cpu_stats = cpu_data[cpu_columns].agg(['mean', 'median', 'max', 'min', 'var']).transpose().reset_index().rename(columns={'index': 'Namespace'})
    
    return memory_stats, cpu_stats

def aggregate_data(base_dir: Path, threads, actions, output_dir: Path):
    """
    ディレクトリ構造に基づいてデータを集計し、結果を保存します。

    Parameters:
        base_dir (Path): データが格納されている基点ディレクトリ
        threads (list): スレッド数のリスト
        actions (list): アクション名のリスト
        output_dir (Path): 集計結果を保存するディレクトリ
    """
    # 結果を格納するリスト
    batch_results = []
    statuscode_results = []
    memory_results = []
    cpu_results = []
    record_counts = []

    for thread in threads:
        for action in actions:
            batch_dir = base_dir / f"thread_{thread}" / action / "batch"
            metrics_dir = base_dir / f"thread_{thread}" / action / "metrics"
            
            # Batchデータの集計
            if batch_dir.exists() and batch_dir.is_dir():
                batch_csv_files = list(batch_dir.glob('*.csv'))
                if batch_csv_files:
                    df_list = []
                    for csv_file in batch_csv_files:
                        try:
                            df = pd.read_csv(csv_file)
                            df_list.append(df)
                        except Exception as e:
                            print(f"CSVの読み込みに失敗しました: {csv_file}. エラー: {e}")
                    
                    if df_list:
                        batch_data = pd.concat(df_list, ignore_index=True)
                        record_count = len(batch_data)
                        batch_stats, statuscode_counts = create_aggregate_batch(batch_data)
                        
                        # Batch統計結果をリストに追加
                        batch_results.append({
                            'Thread': thread,
                            'Action': action,
                            'Count': batch_stats['Count'],
                            'Mean_ResponseTime_ms': batch_stats['Mean'],
                            'Median_ResponseTime_ms': batch_stats['Median'],
                            'Max_ResponseTime_ms': batch_stats['Max'],
                            'Min_ResponseTime_ms': batch_stats['Min'],
                            'Variance_ResponseTime_ms': batch_stats['Variance']
                        })
                        
                        # Record countを記録
                        record_counts.append({
                            'Thread': thread,
                            'Action': action,
                            'RecordCount': record_count
                        })
            
            # Metricsデータの集計
            if metrics_dir.exists() and metrics_dir.is_dir():
                memory_csv = metrics_dir / "metrics_memory_by_namespace.csv"
                cpu_csv = metrics_dir / "metrics_service_app_cpu_by_namespace_rate.csv"
                
                if memory_csv.exists() and cpu_csv.exists():
                    try:
                        memory_data = pd.read_csv(memory_csv)
                        cpu_data = pd.read_csv(cpu_csv)
                        
                        memory_stats, cpu_stats = create_aggregate_metrics(memory_data, cpu_data)
                        
                        # スレッドとアクション情報を追加
                        memory_stats['Thread'] = thread
                        memory_stats['Action'] = action
                        cpu_stats['Thread'] = thread
                        cpu_stats['Action'] = action
                        
                        # 結果をリストに追加
                        memory_results.append(memory_stats)
                        cpu_results.append(cpu_stats)
                    except Exception as e:
                        print(f"Metrics CSVの読み込みに失敗しました: {metrics_dir}. エラー: {e}")

    # DataFrame化
    df_batch = pd.DataFrame(batch_results)
    df_statuscode = pd.DataFrame(statuscode_results)
    df_memory = pd.concat(memory_results, ignore_index=True) if memory_results else pd.DataFrame()
    df_cpu = pd.concat(cpu_results, ignore_index=True) if cpu_results else pd.DataFrame()
    df_record_counts = pd.DataFrame(record_counts)
    
    # 集計結果を保存
    output_dir.mkdir(parents=True, exist_ok=True)
    
    df_batch.to_csv(output_dir / 'batch_response_stats.csv', index=False)
    # df_statuscode.to_csv(output_dir / 'batch_statuscode_counts.csv', index=False)
    df_memory.to_csv(output_dir / 'metrics_memory_stats.csv', index=False)
    df_cpu.to_csv(output_dir / 'metrics_cpu_stats.csv', index=False)
    df_record_counts.to_csv(output_dir / 'record_counts.csv', index=False)
    
    print(f"集計が完了しました。結果は '{output_dir}' に保存されました。")

def main():
    parser = argparse.ArgumentParser(description="CSVファイルのResponseTimeとStatusCode、およびNamespaceごとのCPUとMemory使用量を集計します。")
    parser.add_argument('base_directory', type=str, help='データが格納されている基点ディレクトリのパス')
    parser.add_argument('output_directory', type=str, help='集計結果を保存するディレクトリのパス')
    args = parser.parse_args()
    
    base_dir = Path(args.base_directory).resolve()
    output_dir = Path(args.output_directory).resolve()
    
    # スレッド数とアクション名の定義
    threads = [10, 50, 100]
    # actions = ["create_user_profile", "create_file_object", "create_organization"]
    actions = ["type1", "type2", "type3"]
    
    aggregate_data(base_dir, threads, actions, output_dir)

if __name__ == "__main__":
    main()
