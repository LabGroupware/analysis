import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_stacked_bar_grids(data_sets, last_data, n_cols=2, figsize=(10, 5)):
    n_rows = int(np.ceil(len(data_sets) / n_cols))  # 必要な行数
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(figsize[0] * n_cols, figsize[1] * n_rows), squeeze=False)

    for idx, (data, title) in enumerate(data_sets):
        ax = axes[idx // n_cols, idx % n_cols]

        sorted_columns = ["Key"] + sorted(data.columns[1:], key=int)
        data = data[sorted_columns]
        # keys = data.iloc[:, 0]  # 1列目 (x軸の値)
        # categories = data.columns[1:]  # 2列目以降 (カテゴリ)
        actions = data.iloc[:, 0]
        threads = data.columns[1:]

        x = np.arange(len(threads)) * 1.5
        bar_bottoms = np.zeros(len(threads))  # 積み上げ棒グラフの初期値

        # 各カテゴリを積み上げ
        for idx, action in enumerate(actions):
            ax.bar(
                x, 
                data.iloc[idx, 1:], 
                bottom=bar_bottoms, 
                width=0.8,
                label=action
            )
            bar_bottoms += data.iloc[idx, 1:]

        # グラフの装飾
        ax.set_xticks(x)
        ax.set_xticklabels(threads)
        ax.set_title(title)
        ax.set_xlabel("Threads")
        ax.set_ylabel("Time (ms)")
        ax.legend(title="Process", loc="upper left", fontsize=5, framealpha=0.5)

    print(last_data)
    
    # 並び替え
    last_data = last_data[sorted(last_data.columns, key=int)]

    print(last_data)

        # LastDataのプロット
    threads = last_data.columns.astype(int)
    actions = last_data.index

    for action in actions:
        ax = axes[len(data_sets) // n_cols, len(data_sets) % n_cols]
        ax.plot(threads, last_data.loc[action], marker="o", label=action)
        ax.set_xticks(threads)
        ax.legend(title="Action", loc="upper left", fontsize=5, framealpha=0.5)
        ax.set_title("TotalTime")
        ax.set_xlabel("Threads")
        ax.set_ylabel("Time (ms)")

    # 不要なサブプロットを非表示
    for idx in range(len(data_sets) + 1, n_rows * n_cols):
        fig.delaxes(axes[idx // n_cols, idx % n_cols])

    plt.tight_layout()
    plt.subplots_adjust(right=0.95)
    plt.show()
