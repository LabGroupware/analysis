import pandas as pd
from pathlib import Path
from metrics import ScenarioMetrics
from utils import bytes_to_human_readable

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

base_dir = Path('./rci')
thread_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name.startswith('thread_')]
scenarios = [
    "sc1", "sc2", "sc3", "sc4", "sc5", "sc6", "sc7", "sc8", "sc9", "sc10",
    "sc11", "sc12", "sc13", "sc14", "sc15", "sc16", "sc17", "sc18", "sc19", "sc20",
    "sc21", "sc22", "sc23", "sc24", "sc25", "sc26", "sc27"
]

scenario_occurs_rate = [
    0.03, 0.0333, 0.02, 0.0333, 0.0467, 0.0333, 0.04, 0.0333, 0.0467, 0.0333,
    0.04, 0.0333, 0.0333, 0.04, 0.04, 0.04, 0.0333, 0.04, 0.0467, 0.0333, 
    0.0333, 0.0467, 0.0267, 0.04, 0.04, 0.05, 0.0333
]

scenario_occurs_rate_map = dict(zip(scenarios, scenario_occurs_rate))

metrics_lists = ['cpu_rate', 'memory', 'db_cpu_rate', 'db_memory']
namespaces = ["UserProfile", "UserPreference", "Organization", "Team", "Plan", "Storage"]

related_scenarios_map = {
    "UserProfile": ["sc1", "sc3", "sc4", "sc8", "sc10", "sc11", "sc13", "sc15", "sc17", "sc19", "sc21"],
    "UserPreference": ["sc1", "sc2", "sc12", "sc13"],
    "Organization": ["sc3", "sc4", "sc6", "sc7", "sc18", "sc19", "sc20", "sc21"],
    "Team": ["sc3", "sc4", "sc6", "sc7", "sc8", "sc14", "sc15", "sc16", "sc17"],
    "Plan": ["sc8", "sc9", "sc24", "sc25", "sc26", "sc27"],
    "Storage": ["sc5", "sc8", "sc22", "sc23", "sc25", "sc27"]
}

result = {}

aggregate_results = {}
threads = []
for t_dir in thread_dirs:
    thread_count = int(t_dir.name.replace('thread_', ''))
    aggregate_results[thread_count] = {}
    threads.append(thread_count)
    for scenario in scenarios:
        scenario_dir = t_dir / scenario
        if not scenario_dir.exists():
            continue

        metrics_map = {}
        for metrics in metrics_lists:
            metrics_dir = scenario_dir / metrics
            if not metrics_dir.exists():
                continue

            df_list = []
            # csvファイルは一つのみと仮定
            csv_file = list(metrics_dir.glob("*.csv"))[0]
            df = pd.read_csv(csv_file)
            # if metrics == 'memory' or metrics == 'db_memory':
            #     metrics_map[metrics] = df[namespaces].max()
            # else:
            #     metrics_map[metrics] = df[namespaces].max() * 1000
            metrics_map[metrics] = df[namespaces].max()
        
        aggregate_results[thread_count][scenario] = metrics_map

for th in threads:
    result[th] = {
        "metricsMaps": {},
        "metricsAppMaps": {},
        "metricsDBMaps": {},
    }
    for ns in namespaces:
        result[th]["metricsMaps"][ns] = {}
        result[th]["metricsAppMaps"][ns] = {}
        result[th]["metricsDBMaps"][ns] = {}
        need_scenarios = related_scenarios_map[ns]
        for sc in need_scenarios:
            result[th]["metricsMaps"][ns][sc] = {}
            result[th]["metricsAppMaps"][ns][sc] = {}
            result[th]["metricsDBMaps"][ns][sc] = {}

for thread, scenarios in aggregate_results.items():
    for scenario, metrics in scenarios.items():
        for metric, namespace in metrics.items():
            for ns, v in namespace.items():
                need_scenarios = related_scenarios_map[ns]
                if scenario in need_scenarios:
                    result[thread]["metricsMaps"][ns][scenario][metric] = v
                    if metric.startswith("db_"):
                        result[thread]["metricsDBMaps"][ns][scenario][metric.replace('db_', '')] = v
                    else:
                        result[thread]["metricsAppMaps"][ns][scenario][metric] = v

ret_val = {}

for th in threads:
    ret_val[th] = {}
    for ns in namespaces:
        ret_val[th][ns] = {}


def create_and_print_srci(data: dict, title: str, beta=0.2, gamma=0.8) -> tuple:
    """
    S-RCIを計算し、出力する。
    
    Args:
    data (dict): メトリクスのデータ
    
    Returns:
    float: S-RCI
    """
    scenario_metrics = ScenarioMetrics(data, scenario_occurs_rate_map, title=title, beta=beta, gamma=gamma)
    # print("\nMetric DataFrame:")
    # print(scenario_metrics.get_metrics())
    # ratio_df = scenario_metrics.compute_ratio_dataframe()
    # print("\nRatio DataFrame:")
    # print(ratio_df)
    # 対数変換された比率のデータフレームを計算
    # log_ratio_df = scenario_metrics.compute_log_ratio_dataframe()
    # print("\nLog Ratio DataFrame:")
    # print(log_ratio_df)

    # 共分散行列を計算
    # covariance_matrix = scenario_metrics.compute_covariance_matrix()
    # print("\nCovariance Matrix:")
    # print(covariance_matrix)

    # 共分散行列のトレース/組み合わせ数を計算
    trace_ratio = scenario_metrics.compute_covariance_trace_ratio()
    # print(f"\nS-RCI: {trace_ratio}")

    # Raw K-means
    # clusters = scenario_metrics.k_means_raw_clustering(2)
    # print("\nRaw Clusters:")
    # print(clusters)
    # scenario_metrics.plot_k_means_raw_clustering(2)

    # # K-means
    # clusters = scenario_metrics.k_means_clustering(2)
    # print("\nClusters:")
    # print(clusters)
    # scenario_metrics.plot_k_means_clustering(2)

    # GMM(clusters)
    scenario_metrics.plot_gaussian_mixture_clustering(2)

    each_sum = scenario_metrics.each_metrics_sum()
    return trace_ratio, each_sum

for th, maps in result.items():
    print(f"\n==================== Thread: {th} ====================")
    for ns, v in maps['metricsMaps'].items():
        print(f"\n~~~~~~~~~~~~~~~~~~~~ Namespace: {ns} ~~~~~~~~~~~~~~~~~~~~")
        srci, sums = create_and_print_srci(v, ns)
        ret_val[th][ns]["All"] = srci
        sums_keys = list(sums.keys())
        for k in sums_keys:
            if "memory" in k:
                ret_val[th][ns][f"{k}_sum"] = bytes_to_human_readable(sums[k])
            else:
                ret_val[th][ns][f"{k}_sum"] = sums[k]
    # # App Metrics
    # for ns, v in maps['metricsAppMaps'].items():
    #     print(f"\n~~~~~~~~~~~~~~~~~~~~ Namespace: {ns}(Application) ~~~~~~~~~~~~~~~~~~~~")
    #     srci, _ = create_and_print_srci(v, ns)
    #     ret_val[th][ns]["Application"] = srci
    # # DB Metrics
    # for ns, v in maps['metricsDBMaps'].items():
    #     print(f"\n~~~~~~~~~~~~~~~~~~~~ Namespace: {ns}(DB) ~~~~~~~~~~~~~~~~~~~~")
    #     srci, _ = create_and_print_srci(v, ns)
    #     ret_val[th][ns]["DB"] = srci

for th, ns_val in ret_val.items():
    # print(f"\n==================== Thread: {th} ====================")
    sum_columns = []
    for met in metrics_lists:
        sum_columns.append(f"{met}_sum")
    val_df = pd.DataFrame(ns_val, index=["All", "Application", "DB", *sum_columns])
    # print(val_df.T)

beta_lists = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
gamma_lists = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

beta_const = 0.2
gamma_const = 0.4

# beta_change plot
# beta_change = {}
# gamma_change = {}
# for th, maps in result.items():
#     for ns, v in maps['metricsMaps'].items():
#         beta_change[ns] = {}
#         gamma_change[ns] = {}
#         for beta in beta_lists:
#             srci, _ = create_and_print_srci(v, ns, beta=beta, gamma=gamma_const)
#             beta_change[ns][beta] = srci
#         for gamma in gamma_lists:
#             srci, _ = create_and_print_srci(v, ns, beta=beta_const, gamma=gamma)
#             gamma_change[ns][gamma] = srci

# plot
# import matplotlib.pyplot as plt

# # beta 全体プロット
# plt.figure()
# for ns, v in beta_change.items():
#     plt.plot(list(v.keys()), list(v.values()), label=ns)
# plt.title(f"Beta Change")
# plt.xlabel("Beta")
# plt.ylabel("S-RCI")
# plt.legend()
# plt.show()

# # beta 個別プロット
# ax, fig = plt.subplots(2, 3, figsize=(10, 5))
# for i, ns in enumerate(namespaces):
#     ax = fig[i // 3][i % 3]
#     ax.set_title(f"{ns} Beta Change")
#     ax.plot(list(beta_change[ns].keys()), list(beta_change[ns].values()))
#     ax.set_xlabel("Beta")
#     ax.set_ylabel("S-RCI")
# plt.tight_layout()
# plt.show()

# # gamma 全体プロット
# plt.figure()
# for ns, v in gamma_change.items():
#     plt.plot(list(v.keys()), list(v.values()), label=ns)
# plt.title(f"Gamma Change")
# plt.xlabel("Gamma")
# plt.ylabel("S-RCI")
# plt.legend()
# plt.show()

# # gamma 個別プロット
# ax, fig = plt.subplots(2, 3, figsize=(10, 5))
# for i, ns in enumerate(namespaces):
#     ax = fig[i // 3][i % 3]
#     ax.set_title(f"{ns} Gamma Change")
#     ax.plot(list(gamma_change[ns].keys()), list(gamma_change[ns].values()))
#     ax.set_xlabel("Gamma")
#     ax.set_ylabel("S-RCI")
# plt.tight_layout()
# plt.show()
