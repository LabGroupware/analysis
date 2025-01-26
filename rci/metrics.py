import pandas as pd
import itertools
import numpy as np

class ScenarioMetrics:

    def __init__(self, data: dict, scenario_occurs_rate_map: dict, beta: float = 0.5, gamma: float = 0.5, title: str = "Scenario Metrics"):
        """
        コンストラクタ。
        
        Parameters:
        data (dict): シナリオごとのメトリクスデータ。
                     例:
                     {
                         "sc1": {"cpu_rate": 0.1, "memory": 0.1, "gpu": 0.1}, 
                         "sc3": {"cpu_rate": 0.2, "memory": 0.2, "gpu": 0.2}, 
                         ...
                     }
        """
        # データをデータフレームに変換
        self.df = pd.DataFrame.from_dict(data, orient='index')
        self.metrics = sorted(self.df.columns.tolist())  # メトリクス名をソートして保持
        self.metric_pairs = list(itertools.combinations(self.metrics, 2))  # 2項組み合わせを生成
        self.sw = self.compute_scenario_occur_rate_weight(scenario_occurs_rate_map, beta)
        # print(self.sw)
        self.rmw = self.compute_scenario_metrics_weight()
        # print(self.rmw)
        self.gamma = gamma
        self.title = title

    def get_num_metric_combinations(self) -> int:
        """
        メトリクスに関する全2項組み合わせの数を返す。
        
        Returns:
        int: 組み合わせの数
        """
        return len(self.metric_pairs)
    
    def compute_scenario_occur_rate_weight(self, scenario_occurs_rate_map: dict, beta: float) -> dict:
        """
        シナリオの発生率の重みを計算する。
        """
        scenario_list = self.df.index.tolist()
        scenario_occur_rate = np.array([scenario_occurs_rate_map[sc] for sc in scenario_list])
        adjusted_weight = scenario_occur_rate ** beta
        return dict(zip(scenario_list, adjusted_weight))
    
    def compute_scenario_metrics_weight(self) -> pd.DataFrame:
        """
        シナリオごとのメトリクスの重みを計算する。
        """
        column_sums = self.df.sum(axis=0) 
        normalized_df = self.df.div(column_sums, axis=1)
        return normalized_df

    
    def each_metrics_sum(self) -> pd.DataFrame:
        """
        各メトリクスの合計値を計算する。
        
        Returns:
        pd.DataFrame: 各メトリクスの合計値
        """
        return self.df.sum()
    
    def get_metrics(self) -> pd.DataFrame:
        """
        メトリクスのデータフレームを返す。
        
        Returns:
        pd.DataFrame: メトリクスのデータフレーム
        """
        return self.df

    def compute_ratio_dataframe(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        各シナリオにおいて、メトリクスの比率を計算し、新たなデータフレームを作成する。
        比率の順序はメトリクス名のソート順に基づく。
        
        Returns:
        pd.DataFrame: 比率を含む新しいデータフレーム
        """
        ratio_data = {}
        weight_data = {}
        only_rw = {}
        for sc in self.df.index:
            ratios = {}
            weights = {}
            for numerator, denominator in self.metric_pairs:
                ratio_key = f"{numerator}/{denominator}"
                # ゼロ除算を避けるためのチェック
                denominator_value = self.df.at[sc, denominator]
                if denominator_value != 0:
                    ratio_value = self.df.at[sc, numerator] / denominator_value
                else:
                    ratio_value = np.nan  # または適切な値に設定
                ratios[ratio_key] = ratio_value
                rw = (np.sqrt(self.rmw.at[sc, denominator] * self.rmw.at[sc, numerator])) ** self.gamma
                weights[ratio_key] = rw
            ratio_data[sc] = ratios
            sc_weight = self.sw[sc]
            only_rw[sc] = {k: v for k, v in weights.items()}
            weight_data[sc] = {k: v * sc_weight for k, v in weights.items()}
        ratio_df = pd.DataFrame.from_dict(ratio_data, orient='index')
        weight_df = pd.DataFrame.from_dict(weight_data, orient='index')
        only_rw_df = pd.DataFrame.from_dict(only_rw, orient='index')
        only_rw_df["AVG"] = only_rw_df.mean(axis=1)
        # print(only_rw_df)
        n_samples = weight_df.shape[0]
        normalized_W = weight_df * n_samples / np.sum(weight_df, axis=0)
        # print(normalized_W)
        return ratio_df, normalized_W

    def compute_log_ratio_dataframe(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        計算した比率を対数変換したデータフレームを作成する。
        
        Returns:
        pd.DataFrame: 対数変換された比率を含むデータフレーム
        """
        ratio_df, weight_df = self.compute_ratio_dataframe()
        # ゼロや負の値がある場合に対数が定義されないため、適切に処理
        if (ratio_df <= 0).any().any():
            raise ValueError("比率データに0以下の値が含まれています。対数変換できません。")
        log_ratio_df = np.log(ratio_df)
        return log_ratio_df, weight_df
    
    def k_means_raw_clustering(self, n_clusters: int) -> np.ndarray:
        """
        メトリクスのデータフレームをK-meansクラスタリングによりクラスタリングする。
        
        Parameters:
        n_clusters (int): クラスタ数
        
        Returns:
        np.ndarray: クラスタリング結果のラベル
        """
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(self.df)
        return kmeans.labels_
    
    def k_means_clustering(self, n_clusters: int) -> np.ndarray:
        """
        メトリクスのデータフレームをK-meansクラスタリングによりクラスタリングする。
        
        Parameters:
        n_clusters (int): クラスタ数
        
        Returns:
        np.ndarray: クラスタリング結果のラベル
        """
        from sklearn.cluster import KMeans
        log_ratio_df, weight_data = self.compute_log_ratio_dataframe()
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(log_ratio_df)
        return kmeans.labels_
    
    def plot_k_means_raw_clustering(self, n_clusters: int) -> None:
        """
        メトリクスのデータフレームをK-meansクラスタリングによりクラスタリングし、結果をプロットする。
        
        Parameters:
        n_clusters (int): クラスタ数
        """
        import matplotlib.pyplot as plt
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(self.df)
        labels = self.k_means_raw_clustering(n_clusters)
        scenario_list = self.df.index.tolist()
        plt.scatter(pca_result[:, 0], pca_result[:, 1], c=labels)
        for i, txt in enumerate(scenario_list):
            plt.annotate(txt, (pca_result[i, 0], pca_result[i, 1]))
        plt.title(f"K-means Clustering ({self.title})")
        plt.show()
    
    def plot_k_means_clustering(self, n_clusters: int) -> None:
        """
        メトリクスのデータフレームをK-meansクラスタリングによりクラスタリングし、結果をプロットする。
        
        Parameters:
        n_clusters (int): クラスタ数
        """
        import matplotlib.pyplot as plt
        from sklearn.decomposition import PCA
        log_ratio_df, weight_df = self.compute_log_ratio_dataframe()
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(log_ratio_df)
        labels = self.k_means_clustering(n_clusters)
        scenari_list = log_ratio_df.index.tolist()
        plt.scatter(pca_result[:, 0], pca_result[:, 1], c=labels)
        for i, txt in enumerate(scenari_list):
            plt.annotate(txt, (pca_result[i, 0], pca_result[i, 1]))
        plt.title(f"K-means Clustering ({self.title})")
        plt.show()
    
    def plot_gaussian_mixture_clustering(self, n_components: int) -> None:
        """
        メトリクスのデータフレームをガウス混合モデルによりクラスタリングし、結果をプロットする。
        
        Parameters:
        n_components (int): クラスタ数
        """
        import matplotlib.pyplot as plt
        from sklearn.mixture import GaussianMixture
        from matplotlib.colors import Normalize
        X, weight_df = self.compute_log_ratio_dataframe()
        gmm = GaussianMixture(n_components=n_components, random_state=0).fit(X)
        probs = gmm.predict_proba(X)
        labels = gmm.predict(X)
        weights_mean = weight_df.mean(axis=1).to_numpy().reshape(-1, 1)
        zero_centered_probs = (probs - 0.5) * 2
        probs = zero_centered_probs * weights_mean / np.sum(weights_mean)
        probs_max = np.max(probs)
        probs_min = np.min(probs)
        probs = -1 + 2 * (probs - probs_min) / (probs_max - probs_min)
        group_A_probs = probs[:, 0]
        sc_prob_map = dict(zip(X.index.tolist(), group_A_probs))
        sc_prob_map_df = pd.DataFrame.from_dict(sc_prob_map, orient='index', columns=['Group A Probability'])
        print(sc_prob_map_df)
        fig, ax = plt.subplots(figsize=(8, 6))
        norm = Normalize(vmin=-1, vmax=1)
        scatter = ax.scatter(X.iloc[:, 0], X.iloc[:, 1], c=probs[:, 0], cmap='coolwarm', s=50, edgecolor='k', norm=norm)
        centers = gmm.means_
        ax.scatter(centers[:, 0], centers[:, 1], c='yellow', s=120, label='Cluster Centers', edgecolor='k', alpha=0.3)

        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Probability of Cluster 1')

        for i, txt in enumerate(X.index.tolist()):
            ax.annotate(txt, (X.iloc[i, 0], X.iloc[i, 1]))

        plt.title(f"Gaussian Mixture Clustering ({self.title})")
        plt.show()

    def get_log_ratio_matrix(self) -> tuple[np.ndarray, pd.DataFrame]:
        """
        compute_log_ratio_dataframeで出力されたデータフレームを行列（NumPy配列）に変換する。
        
        Returns:
        np.ndarray: 対数比の行列
        """
        log_ratio_df, weight_df = self.compute_log_ratio_dataframe()
        return log_ratio_df.to_numpy(), weight_df

    def compute_column_means(self) -> np.ndarray:
        """
        compute_log_ratio_dataframeで出力されたデータフレームの各メトリクス（列）の平均を計算する。
        
        Returns:
        np.ndarray: 各列の平均値
        """
        log_ratio_df, weight_df = self.compute_log_ratio_dataframe()
        # return np.mean(log_ratio_df.to_numpy(), axis=0)  # 形状: (n_features,)
        return np.average(log_ratio_df.to_numpy(), axis=0, weights=weight_df.to_numpy())

    def compute_covariance_matrix(self) -> np.ndarray:
        """
        compute_log_ratio_dataframeで出力されたデータフレームを基に、共分散行列を作成する。
        指定された式を用いる: Cov(X, Y) = (1/n) * Σ (X_i - μ_X)(Y_i - μ_Y)
        
        Returns:
        np.ndarray: 共分散行列
        """
        X, W = self.get_log_ratio_matrix()  # 形状: (n_samples, n_features), (n_samples, n_features)
        mu = self.compute_column_means()  # 形状: (n_features,)
        deviations = X - mu  # 形状: (n_samples, n_features)
        weighted_deviations = deviations * W
        # covariance_matrix = np.cov(weighted_deviations, rowvar=False, bias=True)  # 形状: (n_features, n_features)
        n_samples = X.shape[0]
        covariance_matrix = (weighted_deviations.T @ weighted_deviations) / n_samples  # 形状: (n_features, n_features)
        # covariance_matrix = (weighted_deviations.T @ deviations) / np.sum(W, axis=0)  # 形状: (n_features, n_features)
        return covariance_matrix

    def compute_covariance_trace_ratio(self) -> float:
        """
        共分散行列のトレース（対角成分の和）を、メトリクスの全2項組み合わせの数で割った値を返す。
        
        Returns:
        float: 共分散行列のトレースを組み合わせ数で割った値
        """
        covariance_matrix = self.compute_covariance_matrix()
        trace = np.trace(covariance_matrix)
        num_combinations = self.get_num_metric_combinations()
        trace_ratio = trace / num_combinations
        return trace_ratio