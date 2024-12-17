import pandas as pd
import os

exclude_namespaces = ['Usage', 'AuthUsage', 'WebsocketUsage', 'WebGatewayUsage', 'JobUsage']

def process_metrics(cpu_file, memory_file):
    # CSVファイルの読み込み
    cpu_df = pd.read_csv(cpu_file)
    memory_df = pd.read_csv(memory_file)

    # max-minのカラム追加
    # for df in [cpu_df, memory_df]:
        # df['max_min_diff'] = df['max'] / df['min']
        # df['max_min_diff'] = df['max'] - df['min']
        # df['max_min_diff'] = df['max']

    # Actionごと、Threadごとにまとめ、(Thread50/Thread10), (Thread100/Thread50) を計算
    def calc_thread_ratio(df, metric):
        pivot_df = df.pivot_table(index=['Namespace', 'Action'], columns='Thread', values=metric)
        pivot_df['Thread50/Thread10'] = pivot_df[50] / pivot_df[10]
        pivot_df['Thread100/Thread50'] = pivot_df[100] / pivot_df[50]
        return pivot_df.reset_index()

    # cpu_ratio = calc_thread_ratio(cpu_df, 'max_min_diff')
    # memory_ratio = calc_thread_ratio(memory_df, 'max_min_diff')

    cpu_ratio = calc_thread_ratio(cpu_df, 'max')
    memory_ratio = calc_thread_ratio(memory_df, 'max')

    cpu_ratio["Namespace"] = cpu_ratio["Namespace"].str.replace("CPUUsage", "Usage")
    memory_ratio["Namespace"] = memory_ratio["Namespace"].str.replace("MemoryUsage", "Usage")

    cpu_ratio = cpu_ratio[~cpu_ratio['Namespace'].isin(exclude_namespaces)]
    memory_ratio = memory_ratio[~memory_ratio['Namespace'].isin(exclude_namespaces)]

    # CPU / Memory の比率計算
    combined_df = cpu_ratio.merge(memory_ratio, on=['Namespace', 'Action'], suffixes=('_CPU', '_Memory'))
    combined_df['Thread50/Thread10_Ratio'] = combined_df['Thread50/Thread10_CPU'] / combined_df['Thread50/Thread10_Memory']
    combined_df['Thread100/Thread50_Ratio'] = combined_df['Thread100/Thread50_CPU'] / combined_df['Thread100/Thread50_Memory']

    return combined_df

def calculate_cv(df, column):
    mean = df[column].mean()
    std = df[column].std()
    cv = std / mean
    return cv

# ファイルパスを指定して実行
cpu_query_file_path = 'metrics/cmd/ag/metrics_cpu_stats.csv'
memory_query_file_path = 'metrics/cmd/ag/metrics_memory_stats.csv'
cpu_cmd_file_path = 'metrics/query/ag/metrics_cpu_stats.csv'
memory_cmd_file_path = 'metrics/query/ag/metrics_memory_stats.csv'
query_result_df = process_metrics(cpu_query_file_path, memory_query_file_path)
cmd_result_df = process_metrics(cpu_cmd_file_path, memory_cmd_file_path)

# 結果をCSVに保存
query_result_df.to_csv('metrics/query/an/metrics_analysis_result.csv', index=False)
cmd_result_df.to_csv('metrics/cmd/an/metrics_analysis_result.csv', index=False)

# query_result_dfとcmd_result_dfをconcat
result_df = pd.concat([query_result_df, cmd_result_df], ignore_index=True)


# 結果をCSVに保存
result_df.to_csv('metrics/an/metrics_analysis_result.csv', index=False)

aggregate_dict = {
    'OrganizationUsage': ['create_organization', 'type3'],
    'StorageUsage': ['create_file_object'],
    'UserProfileUsage': ['create_user_profile', 'create_organization', 'type2'],
    'UserPreferenceUsage': ['create_user_profile', 'type2'],
    'TeamUsage': ['create_organization', 'type1'],
    'PlanUsage': [],
}

t10_t50_dir = 'metrics/an/t10_t50'
os.makedirs(t10_t50_dir, exist_ok=True)
t50_t100_dir = 'metrics/an/t50_t100'
os.makedirs(t50_t100_dir, exist_ok=True)

# Namespaceごとに集計
for namespace, actions in aggregate_dict.items():
    if not actions:
        continue

    filtered_df = result_df[result_df['Namespace'] == namespace]
    if filtered_df.empty:
        continue

    filtered_df = filtered_df[filtered_df['Action'].isin(actions)]
    t10_t_50_ratio = filtered_df[['Action', 'Thread50/Thread10_Ratio']]
    t50_t_100_ratio = filtered_df[['Action', 'Thread100/Thread50_Ratio']]
    # filtered_df.to_csv(f'metrics/an/{namespace}_metrics_analysis_result.csv', index=False)
    t10_t_50_ratio.to_csv(os.path.join(t10_t50_dir, f'{namespace}.csv'), index=False)
    t50_t_100_ratio.to_csv(os.path.join(t50_t100_dir, f'{namespace}.csv'), index=False)

    print(f"Namespace: {namespace}")
    print("=" * 20)
    t10_t50_cv = calculate_cv(t10_t_50_ratio, 'Thread50/Thread10_Ratio')
    t50_t100_cv = calculate_cv(t50_t_100_ratio, 'Thread100/Thread50_Ratio')
    print(f"Thread50/Thread10 CV: {t10_t50_cv}")
    print(f"Thread100/Thread50 CV: {t50_t100_cv}")
    print("=" * 20)