import matplotlib.pyplot as plt
import pandas as pd

def display_results(aggregate_results):
    # ResponseTimeの統計を表示
    response_time_data = []
    for result in aggregate_results:
        response_time_data.append({
            'Thread': result['Thread'],
            'Scenario': result['Scenario'],
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
        print(f"\nThread: {result['Thread']}, Scenario: {result['Scenario']}, RecordCount: {result['RecordCount']}")
        df_status = pd.DataFrame(result['StatusCode_Counts'])
        print(df_status.to_markdown(index=False))

def visualize_results(aggregate_results, scenarios, threads):
    # ResponseTimeの平均をアクションごとにプロット
    plt.figure(figsize=(12, 8))
    
    for scenario in scenarios:
        mean_values = []
        thread_labels = []
        for thread in threads:
            # 該当するアクションとスレッドのデータを取得
            filtered = [res for res in aggregate_results if res['Scenario'] == scenario and res['Thread'] == thread]
            if filtered:
                mean = filtered[0]['ResponseTime_Mean']
                mean_values += [mean]
                thread_labels += [thread]
            

        plt.plot(thread_labels, mean_values, marker='o', label=scenario)
        
    plt.xlabel('Thread Count')
    plt.ylabel('Average ResponseTime (ms)')
    plt.title('Average ResponseTime by Thread Count and Scenario')
    plt.legend()
    plt.grid(True)
    plt.xticks(threads)
    plt.tight_layout()
    plt.show()