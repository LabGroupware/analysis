import pandas as pd
import matplotlib.pyplot as plt

# aggregator.pyで生成されたCSVを読み込み
processed_all = pd.read_csv('aggregate/processed_all.csv').sort_values(by='thread')
success_client_all = pd.read_csv('aggregate/success_client_all.csv').sort_values(by='thread')
success_server_all = pd.read_csv('aggregate/success_server_all.csv').sort_values(by='thread')

# 例えば、JOB_SUCCESSのClientTotalTime_meanをスレッド数で比較する可視化
actions = success_client_all['action'].unique()

# for action in actions:
#     subset = success_client_all[success_client_all['action'] == action].sort_values(by='thread')
#     subset.plot(x='thread', y='ClientTotalTime_mean', marker='o', label=f"{action} (n={subset['record_count'].iloc[0]})")

for action in actions:
    subset = success_client_all[success_client_all['action'] == action].sort_values(by='thread')
    plt.plot(subset['thread'], subset['ClientTotalTime_mean'], marker='o', label=f"{action} (n={subset['record_count'].iloc[0]})")
    # server_subset = success_server_all[success_server_all['action'] == action].sort_values(by='thread')
    # plt.plot(server_subset['thread'], server_subset['SeverTotalTime_mean'], marker='o', label=f"{action} (n={server_subset['record_count'].sum()})")
    # server_subset = success_server_all[success_server_all['action'] == action].sort_values(by='thread')
    # plt.plot(server_subset['thread'], server_subset['SeverTotalTime_var'], marker='o', label=f"{action} (n={server_subset['record_count'].sum()})")
    # server_subset = success_server_all[success_server_all['action'] == action].sort_values(by='thread')
    # plt.plot(server_subset['thread'], server_subset['SeverTotalTime_median'], marker='o', label=f"{action} (n={server_subset['record_count'].sum()})")

plt.xlabel('Thread Count')
plt.ylabel('Client Mean Time (ms)')
plt.title('Client Mean Time by Thread Count and Action (JOB_SUCCESS)')
plt.legend()

plt.show()

# for action in actions:
#     # subset = success_client_all[success_client_all['action'] == action].sort_values(by='thread')
#     # plt.plot(subset['thread'], subset['ClientTotalTime_max'], marker='o', label=f"{action} (n={subset['record_count'].iloc[0]})")
#     subset = success_server_all[success_server_all['action'] == action].sort_values(by='thread')
#     plt.plot(subset['thread'], subset['SeverTotalTime_max'], marker='o', label=f"{action} (n={subset['record_count'].iloc[0]})")

# plt.xlabel('Thread Count')
# plt.ylabel('Max Time (ms)')
# plt.title('Max Time by Thread Count and Action (JOB_SUCCESS)')
# plt.legend()

# plt.show()



# fig, ax = plt.subplots(2,2,figsize=(12,7))
# fig.suptitle('Wait Saga')
# fig.tight_layout()
# fig.subplots_adjust(top=0.85)
# fig.patch.set_facecolor('lightblue')

# for action in actions:
#     subset = success_client_all[success_client_all['action'] == action].sort_values(by='thread')
#     ax[0][0].plot(subset['thread'], subset['ClientTotalTime_mean'], marker='o', label=f"{action} (n={subset['record_count'].iloc[0]})")
#     server_subset = success_server_all[success_server_all['action'] == action].sort_values(by='thread')
#     ax[0][1].plot(server_subset['thread'], server_subset['SeverTotalTime_mean'], marker='o', label=f"{action} (n={server_subset['record_count'].iloc[0]})")

# ax[0][0].set_xlabel('Thread Count')
# ax[0][0].set_ylabel('Average ClientTotalTime (ms)')
# ax[0][0].set_title('Average ClientTotalTime')
# ax[0][0].legend()

# ax[0][1].set_xlabel('Thread Count')
# ax[0][1].set_ylabel('Average ServerTotalTime (ms)')
# ax[0][1].set_title('Average ServerTotalTime')
# ax[0][1].legend()


# for action in actions:
#     subset = success_client_all[success_client_all['action'] == action]
#     print(subset.sort_values(by='thread'))
