'''
萱的源文件，这个.py文件只用来保存学习后的.joblib模型文件
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

import os
os.system('pip install category_encoders==2.6.0')

df = pd.read_csv('car_sales_2014_2015.csv')
df.dropna(inplace=True)
df.drop(['trim','vin','mmr','saledate','seller'],axis=1,inplace=True)



##### Encoding #####
import category_encoders as ce

df_copy = df.copy()

encoder = ce.BinaryEncoder(cols=['year','make','model','body','transmission','interior','color','state'],drop_invariant=True).fit(df_copy)
df_copy = encoder.transform(df_copy)
##### Encoding #####




##### Prediction #####
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import silhouette_score, mean_squared_error, mean_absolute_error, r2_score
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import os
from datetime import datetime
import joblib
import sklearn
class CarAnalyzer:
    def __init__(self, data):
        """Initialize with pre-encoded data"""
        self.data = data
        self.scaler = StandardScaler()
        self.models = {}
        self.numeric_features = ['condition', 'odometer']  # Track numeric features for scaling

    def scale_numeric_features(self):
        """Scale numeric features using StandardScaler and save the scaler"""
        self.data[self.numeric_features] = self.scaler.fit_transform(self.data[self.numeric_features])
        return self.data

    def train_price_prediction_models(self, test_size=0.2):
        """Train multiple price prediction models including Linear Regression"""

        y = self.data['sellingprice']
        X = self.data.drop(['sellingprice'], axis=1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        models = {}
        predictions = {}
        feature_importance = {}

        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        models['LR'] = lr_model
        predictions['LR'] = lr_model.predict(X_test)
        feature_importance['LR'] = pd.Series(np.abs(lr_model.coef_), index=X_train.columns)

        rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        rf_model.fit(X_train, y_train)
        models['RF'] = rf_model
        predictions['RF'] = rf_model.predict(X_test)
        feature_importance['RF'] = pd.Series(rf_model.feature_importances_, index=X_train.columns)

        lgb_model = lgb.LGBMRegressor(random_state=42)
        lgb_model.fit(X_train, y_train)
        models['LGBM'] = lgb_model
        predictions['LGBM'] = lgb_model.predict(X_test)
        feature_importance['LGBM'] = pd.Series(lgb_model.feature_importances_, index=X_train.columns)

        xgb_model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
        )
        xgb_model.fit(X_train, y_train)
        models['XGB'] = xgb_model
        predictions['XGB'] = xgb_model.predict(X_test)
        feature_importance['XGB'] = pd.Series(xgb_model.feature_importances_, index=X_train.columns)


        metrics = {}
        for model_name, y_pred in predictions.items():
            metrics[model_name] = {
                'R2': r2_score(y_test, y_pred),
                'MSE': mean_squared_error(y_test, y_pred),
                'MAE': mean_absolute_error(y_test, y_pred),
                'RMSE': np.sqrt(mean_squared_error(y_test, y_pred))
            }

        self.models = models
        return {
            'models': models,
            'metrics': metrics,
            'feature_importance': feature_importance,
            'test_data': (X_test, y_test)
        }

    def predict_price(self, features_dict):
      """Predict vehicle price using trained models with real-world inputs"""
      if not self.models:
          raise ValueError("Models not trained. Call train_price_prediction_models() first.")


      trained_features = self.data.drop('sellingprice', axis=1).columns.tolist()

      input_df = pd.DataFrame(0, index=[0], columns=trained_features)


      for feature, value in features_dict.items():
          if feature in input_df.columns:
              input_df[feature] = value
          else:
              print(f"Warning: Ignoring unrecognized feature '{feature}'")


      if self.numeric_features:
          input_df[self.numeric_features] = self.scaler.transform(input_df[self.numeric_features])

      predictions = {}
      for model_name, model in self.models.items():
          try:

              X_input = input_df.values


              pred = model.predict(X_input)[0]


              if model_name == 'RF':

                  bootstrap_preds = [tree.predict(X_input)[0] for tree in model.estimators_]
                  lower = np.percentile(bootstrap_preds, 2.5)
                  upper = np.percentile(bootstrap_preds, 97.5)

              elif model_name == 'LR':

                  X_train = self.data.drop('sellingprice', axis=1).values
                  X_design = np.c_[np.ones(len(X_train)), X_train]

                  try:
                      cov_matrix = np.linalg.inv(X_design.T @ X_design)
                  except np.linalg.LinAlgError:
                      cov_matrix = np.linalg.pinv(X_design.T @ X_design)


                  x_new = np.r_[1, X_input[0]]
                  var_pred = x_new @ cov_matrix @ x_new.T
                  mse = mean_squared_error(self.data['sellingprice'], model.predict(X_train))
                  stderr_pred = np.sqrt(mse * (1 + var_pred))

                  lower = pred - 1.96 * stderr_pred
                  upper = pred + 1.96 * stderr_pred

              elif model_name == 'LGBM':
                  num_iterations = model.n_estimators_


                  bootstrap_preds = [
                      model.predict(X_input, num_iteration=i+1)[0]
                      for i in range(num_iterations)
                  ]


                  if not bootstrap_preds:
                      raise ValueError("LightGBM failed to generate bootstrap predictions")

                  lower = np.percentile(bootstrap_preds, 2.5)
                  upper = np.percentile(bootstrap_preds, 97.5)
              elif model_name == 'XGB':

                  n_bootstrap = 100
                  bootstrap_preds = []
                  for _ in range(n_bootstrap):

                      sample_idx = np.random.choice(len(X_input), size=len(X_input), replace=True)
                      X_sample = X_input[sample_idx]
                      pred_sample = model.predict(X_sample)
                      bootstrap_preds.append(pred_sample.mean())

                  lower = np.percentile(bootstrap_preds, 2.5)
                  upper = np.percentile(bootstrap_preds, 97.5)

              else:
                  lower = upper = pred

              predictions[model_name] = {
                  'prediction': float(pred),
                  'lower_bound': float(lower),
                  'upper_bound': float(upper)
              }
          except Exception as e:
              raise ValueError(f"Prediction failed for {model_name}: {str(e)}")

      return predictions

    def analyze_feature_importance(self, top_n=10):
        """Analyze feature importance for all models"""
        if not self.models:
            raise ValueError("Models have not been trained yet. Call train_price_prediction_models first.")

        feature_importance = {}
        for model_name, model in self.models.items():
            if model_name == 'LR':
                importance = pd.Series(
                    np.abs(model.coef_),
                    index=self.data.drop('sellingprice', axis=1).columns,
                    name='importance'
                )
            else:
                importance = pd.Series(
                    model.feature_importances_,
                    index=self.data.drop('sellingprice', axis=1).columns,
                    name='importance'
                )

            feature_importance[model_name] = importance.sort_values(ascending=False).head(top_n)

        return feature_importance

    def plot_feature_importance(analyzer):
        """Plot feature importance for all models"""
        feature_importance = analyzer.analyze_feature_importance(top_n=15)

        for model_name, importance in feature_importance.items():
            plt.figure(figsize=(12, 8))
            ax = importance.plot(kind='barh')
            plt.title(f'Top 15 Important Features ({model_name})')
            plt.xlabel('Feature Importance')

            for i, v in enumerate(importance):
                ax.text(v, i, f'{v:.4f}', va='center')

            plt.tight_layout()
            plt.show()

            print(f"\n{model_name} Feature Importance:")
            for feat, imp in importance.items():
                print(f"{feat}: {imp:.4f}")


    def save_models(self, save_dir="saved_models", tag=""):
        """Save all trained models and preprocessing tools
        Args:
            save_dir (str): Directory to save models
            tag (str): Custom identifier (optional)
        Returns:
            str: Path to saved model file
        """
        # Create directory if not exists
        os.makedirs(save_dir, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"car_models_{timestamp}"
        if tag:
            filename += f"_{tag}"
        save_path = os.path.join(save_dir, filename + ".joblib")

        save_data = {
            'models': self.models,
            'scaler': self.scaler,
            'numeric_features': self.numeric_features,
            'trained_features': self.data.drop('sellingprice', axis=1).columns.tolist(),
            'metadata': {
                'creation_time': timestamp,
                'library_versions': {
                    'sklearn': sklearn.__version__,
                    'xgboost': xgb.__version__,
                    'lightgbm': lgb.__version__,
                    'pandas': pd.__version__
                }
            }
        }


        joblib.dump(save_data, save_path)
        print(f"✅ Models saved successfully! Path: {save_path}")
        return save_path

    @classmethod
    def load_models(cls, model_path):
        """Load trained models from file
        Args:
            model_path (str): Path to model file
        Returns:
            CarAnalyzer: Loaded instance with restored models
        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")


        loaded_data = joblib.load(model_path)


        analyzer = cls(pd.DataFrame(columns=loaded_data['trained_features'] + ['sellingprice']))
        analyzer.models = loaded_data['models']
        analyzer.scaler = loaded_data['scaler']
        analyzer.numeric_features = loaded_data['numeric_features']


        meta = loaded_data['metadata']
        print(f"⏰ Model saved at: {meta['creation_time']}")
        print("📚 Library versions:")
        for lib, ver in meta['library_versions'].items():
            print(f"  - {lib}: {ver}")

        return analyzer



##### Predict #####
analyzer = CarAnalyzer(df_copy)
analyzer.scale_numeric_features()

model_results = analyzer.train_price_prediction_models()
saved_path = analyzer.save_models(tag="v1")
print("\nModel Performance Metrics:")
for model_name, metrics in model_results['metrics'].items():
    print(f"\n{model_name} Model:")
    for metric_name, value in metrics.items():
        print(f"{metric_name}: {value:.4f}")

analyzer.plot_feature_importance()



feature_names = [col for col in analyzer.data.columns
                if col not in ['sellingprice']]

example_car = {feature: 0 for feature in feature_names}

example_car.update({
    'condition': 20,
    'odometer': 75000,
    'state_5': 1,
    'model_6': 1,
    'body_4': 1,
})

print("\nInput features:")
for name, value in example_car.items():
    if value != 0:
        print(f"{name}: {value}")

predictions = analyzer.predict_price(example_car)
print("\nPredictions:")
for model_name, pred in predictions.items():
    print(f"\n{model_name} Model:")
    print(f"Predicted Price: ${pred['prediction']:,.2f}")
    print(f"95% Confidence Interval: (${pred['lower_bound']:,.2f}, ${pred['upper_bound']:,.2f})")
