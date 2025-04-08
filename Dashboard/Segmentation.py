'''
这个目前就设计了一种segmentation，不需要接口，前端可以直接固定
如果在前端想设计一个自由选择n clusters的图的话，可以和萱讨论一下
我在这边应该没有必要做一个接口给出每一个样本点的具体坐标
'''

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pylab as pl
import numpy as np

from sklearn.metrics import mean_squared_error, mean_squared_log_error, mean_absolute_error
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV

import statsmodels.api as sm
from scipy.stats import gaussian_kde
from statsmodels.stats import diagnostic

from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction import FeatureHasher
from sklearn.experimental import enable_iterative_imputer
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor



plt.style.use('dark_background')
from sklearn.linear_model import LinearRegression
import xgboost as xgb

df = pd.read_csv('car_sales_2014_2015.csv')
df.dropna(inplace=True)
df.drop(['trim','vin','mmr','saledate','seller'],axis=1,inplace=True)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

class PriceClusterAnalyzer:
    """
    A clustering analyzer for vehicle pricing data with dynamic feature selection

    Parameters:
    df -- Preprocessed DataFrame containing required features
    x_feature -- Horizontal axis feature (default: 'odometer')
                 Options: 'odometer', 'year', 'condition'
    """

    def __init__(self, df, x_feature='odometer'):
        self.df = df.copy()
        self.x_feature = x_feature
        self.y_feature = 'sellingprice'
        self._validate_features()
        self._filter_outliers()
        self._check_data_adequacy()
        self.scaler = StandardScaler()
        self.kmeans = None
        self.labels = None
        self.centroids = None

    def _validate_features(self):
        """Validate required features exist in DataFrame"""
        required_features = [self.x_feature, self.y_feature]
        missing = [f for f in required_features if f not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required features: {missing}")
        if not all(self.df[required_features].dtypes.apply(np.issubdtype, args=(np.number,))):
            raise ValueError("All features must be numeric")

    def _filter_outliers(self):
        """Dynamic outlier filtering with unit validation"""
        original_size = len(self.df)


        x_stats = self.df[self.x_feature].describe()
        y_stats = self.df[self.y_feature].describe()


        if self.x_feature == 'condition':

            if y_stats['max'] < 1000:
                raise ValueError("Selling price units appear abnormal (max < $1000). Check data unit.")


            filtered = self.df[self.y_feature] <= 80000
            self.df = self.df[filtered]
            print(f"Price filtering: Removed {original_size - len(self.df)} records")

        elif self.x_feature == 'odometer':

            if x_stats['max'] < 1:
                print("Warning: Odometer values appear normalized (max < 1). Adjusting filter threshold.")
                threshold = 0.15
            else:

                threshold = 120000
                print(f"Applying odometer threshold: {threshold:,} miles")

            filtered = self.df[self.x_feature] <= threshold
            self.df = self.df[filtered]
            print(f"Odometer filtering: Removed {original_size - len(self.df)} records")

    def _check_data_adequacy(self):

        if len(self.df) == 0:
            raise ValueError("No data remaining after filtering. Check filter thresholds and data units.")
        if len(self.df) < 50:
            warnings.warn(f"Low sample size after filtering ({len(self.df)} records). Results may be unreliable.")



    def perform_clustering(self, n_clusters=4):
        """Execute K-means clustering with selected features"""

        features = [self.x_feature, self.y_feature]
        scaled_data = self.scaler.fit_transform(self.df[features])

        # Perform K-means clustering
        self.kmeans = KMeans(n_clusters=n_clusters,
                            init='k-means++',
                            n_init=10,
                            random_state=42)
        self.labels = self.kmeans.fit_predict(scaled_data)

        # Calculate centroids in original scale
        self.centroids = self.scaler.inverse_transform(self.kmeans.cluster_centers_)
        return self


    def visualize_clusters(self, figsize=(10,6), save_path=None):
      """Generate cluster visualization plot"""
      if self.kmeans is None:
          raise ValueError("Clustering not performed yet. Call perform_clustering() first")

      plt.figure(figsize=figsize)


      cmap = plt.cm.get_cmap('tab10', 3)

      # Create scatter plot
      scatter = plt.scatter(
          self.df[self.x_feature],
          self.df[self.y_feature],
          c=self.labels,
          cmap=cmap,
          alpha=0.6,
          edgecolors='w',
          s=50,
          vmin=-0.5,
          vmax=2.5
      )

      # Plot cluster centers
      plt.scatter(
          self.centroids[:, 0],
          self.centroids[:, 1],
          marker='o',
          s=200,
          edgecolors='red',
          facecolors='none',
          linewidths=2,
          label='Cluster Centers'
      )


      cbar = plt.colorbar(scatter, ticks=[0, 1, 2])
      cbar.ax.set_yticklabels(['Cluster 0', 'Cluster 1', 'Cluster 2'])

      plt.title(f'Vehicle Price Clustering ({self.x_feature} vs {self.y_feature})')
      plt.xlabel(self._format_label(self.x_feature))
      plt.ylabel(self._format_label(self.y_feature))
      plt.grid(True, linestyle='--', alpha=0.6)
      plt.legend()

      if save_path:
          plt.savefig(save_path, dpi=300, bbox_inches='tight')
      plt.show()
    def _format_label(self, feature):
        """Format axis labels for display"""
        labels = {
            'odometer': 'Odometer',
            'year': 'Manufacture Year',
            'condition': 'Condition Score',
            'sellingprice': 'Selling Price ($)'
        }
        return labels.get(feature, feature.replace('_', ' ').title())

    def generate_report(self):
        """Generate clustering analysis report"""
        if self.kmeans is None:
            raise ValueError("Clustering not performed yet. Call perform_clustering() first")

        return {
            'x_feature': self.x_feature,
            'y_feature': self.y_feature,
            'n_clusters': self.kmeans.n_clusters,
            'silhouette_score': silhouette_score(
                self.df[[self.x_feature, self.y_feature]],
                self.labels
            ),
            'cluster_distribution': pd.Series(self.labels).value_counts().sort_index().to_dict(),
            'centroids': pd.DataFrame(
                self.centroids,
                columns=[self.x_feature, self.y_feature]
            ).round(2).to_dict(orient='records')
        }


if __name__ == "__main__":

    analyzer = PriceClusterAnalyzer(df, x_feature='odometer')


    analyzer.perform_clustering(n_clusters=3)


    analyzer.visualize_clusters(save_path='odometer_clusters.png')

    report = analyzer.generate_report()
    print(f"Silhouette Score: {report['silhouette_score']:.3f}")
    print("\nCluster Distribution:")
    for cluster, count in report['cluster_distribution'].items():
        print(f"Cluster {cluster}: {count} vehicles")

    print("\nCluster Centroids:")
    print(pd.DataFrame(report['centroids']))

