import pandas as pd
from pathlib import Path
import argparse

def load_aggregated_data(output_dir: Path):
    """
    集計結果のCSVファイルを読み込む関数。

    Parameters:
        output_dir (Path): 集計結果が保存されているディレクトリ

    Returns:
        df_batch (pd.DataFrame): Batch ResponseTimeの統計データ
        df_memory (pd.DataFrame): Metrics Memory使用量の統計データ
        df_cpu (pd.DataFrame): Metrics CPU使用量の統計データ
        df_record_counts (pd.DataFrame): アクションごとのデータ件数
    """
    df_batch = pd.read_csv(output_dir / 'batch_response_stats.csv') if (output_dir / 'batch_response_stats.csv').exists() else pd.DataFrame()
    df_memory = pd.read_csv(output_dir / 'metrics_memory_stats.csv') if (output_dir / 'metrics_memory_stats.csv').exists() else pd.DataFrame()
    df_cpu = pd.read_csv(output_dir / 'metrics_cpu_stats.csv') if (output_dir / 'metrics_cpu_stats.csv').exists() else pd.DataFrame()
    df_record_counts = pd.read_csv(output_dir / 'record_counts.csv') if (output_dir / 'record_counts.csv').exists() else pd.DataFrame()
    
    return df_batch, df_memory, df_cpu, df_record_counts

def display_response_time_stats(df_batch):
    """
    ResponseTimeの統計を表形式で表示する関数。

    Parameters:
        df_batch (pd.DataFrame): Batch ResponseTimeの統計データ
    """
    if df_batch.empty:
        print("ResponseTimeの統計データが存在しません。")
        return
    
    print("\n=== ResponseTimeの統計 ===")
    # 適切な桁数で表示
    pd.set_option('display.float_format', '{:.2f}'.format)
    print(df_batch.to_markdown(index=False))

def display_metrics_memory_stats(df_memory):
    """
    Memory使用量の統計を表形式で表示する関数。

    Parameters:
        df_memory (pd.DataFrame): Metrics Memory使用量の統計データ
    """
    if df_memory.empty:
        print("Memory使用量の統計データが存在しません。")
        return
    
    print("\n=== Metrics Memory使用量の統計 ===")
    # 適切な桁数で表示
    pd.set_option('display.float_format', '{:.2f}'.format)
    print(df_memory.to_markdown(index=False))

def display_metrics_cpu_stats(df_cpu):
    """
    CPU使用量の統計を表形式で表示する関数。

    Parameters:
        df_cpu (pd.DataFrame): Metrics CPU使用量の統計データ
    """
    if df_cpu.empty:
        print("CPU使用量の統計データが存在しません。")
        return
    
    print("\n=== Metrics CPU使用量の統計 ===")
    # 適切な桁数で表示
    pd.set_option('display.float_format', '{:.2f}'.format)
    print(df_cpu.to_markdown(index=False))

def display_record_counts(df_record_counts):
    """
    アクションごとのデータ件数を表形式で表示する関数。

    Parameters:
        df_record_counts (pd.DataFrame): アクションごとのデータ件数
    """
    if df_record_counts.empty:
        print("アクションごとのデータ件数のデータが存在しません。")
        return
    
    print("\n=== アクションごとのデータ件数 ===")
    print(df_record_counts.to_markdown(index=False))

def main():
    # コマンドライン引数の設定
    parser = argparse.ArgumentParser(description="集計されたデータを表形式で表示します。")
    parser.add_argument('output_directory', type=str, help='集計結果が保存されているディレクトリのパス')
    args = parser.parse_args()
    
    output_dir = Path(args.output_directory).resolve()
    
    # 集計結果の読み込み
    df_batch, df_memory, df_cpu, df_record_counts = load_aggregated_data(output_dir)
    
    if df_batch.empty and df_memory.empty and df_cpu.empty and df_record_counts.empty:
        print("集計結果のCSVファイルが見つかりません。`aggregate_data.py` を実行してください。")
        return
    
    # 集計結果を表形式で表示
    display_response_time_stats(df_batch)
    display_metrics_memory_stats(df_memory)
    display_metrics_cpu_stats(df_cpu)
    display_record_counts(df_record_counts)

if __name__ == "__main__":
    main()
