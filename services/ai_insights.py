import pandas as pd
import joblib
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import shap
import dask.dataframe as dd
from utils.logger import app_logger
from services.data_service import DataService
from typing import List
import os
from config.settings import settings


class AIInsights:
    """Service for AI-powered insights with explainability."""

    def __init__(self):
        self.data_service = DataService()
        self.scaler = StandardScaler()
        self.sales_model_path = os.path.join(settings.AI_MODELS_PATH, 'sales_model.pkl')
        self.kmeans_model_path = os.path.join(settings.AI_MODELS_PATH, 'kmeans_model.pkl')
        self.sales_model = self.load_model(self.sales_model_path)
        self.kmeans_model = self.load_model(self.kmeans_model_path)
        self.explainer = None

    def load_model(self, model_path):
        """Loads a persisted model if available."""
        if os.path.exists(model_path):
            return joblib.load(model_path)
        return None

    def save_model(self, model, model_path):
        """Saves a model to disk."""
        joblib.dump(model, model_path)

    def train_sales_forecast_model(self):
        """Trains and saves a linear regression model for sales forecasting."""
        orders = self.data_service.get_all_sales_orders(limit=1000)
        df = pd.DataFrame([{
            "date": order.created_at,
            "total": sum([item.quantity * item.price for item in order.items])
        } for order in orders])
        if df.empty:
            app_logger.warning("No data available for training sales forecast model")
            return
        df.sort_values('date', inplace=True)
        df['date_ordinal'] = pd.to_datetime(df['date']).map(pd.Timestamp.toordinal)
        X = df[['date_ordinal']]
        y = df['total']
        self.sales_model = LinearRegression()
        self.sales_model.fit(X, y)
        self.save_model(self.sales_model, self.sales_model_path)
        self.explainer = shap.LinearExplainer(self.sales_model, X)
        app_logger.info("Sales forecast model trained and saved")

    def predict_sales(self, future_dates: List[str]) -> List[float]:
        """Predicts future sales based on the trained model."""
        if not self.sales_model:
            self.train_sales_forecast_model()
        date_ordinal = pd.to_datetime(future_dates).map(pd.Timestamp.toordinal)
        X_future = pd.DataFrame({'date_ordinal': date_ordinal})
        predictions = self.sales_model.predict(X_future)
        return predictions.tolist()

    def explain_predictions(self, future_dates: List[str]):
        """Provides explanations for the predictions."""
        date_ordinal = pd.to_datetime(future_dates).map(pd.Timestamp.toordinal)
        X_future = pd.DataFrame({'date_ordinal': date_ordinal})
        shap_values = self.explainer.shap_values(X_future)
        return shap_values

    def train_customer_segmentation_model(self):
        """Trains and saves a KMeans clustering model for customer segmentation."""
        orders = self.data_service.get_all_sales_orders(limit=10000)
        df = dd.from_pandas(pd.DataFrame([{
            "customer_name": order.customer_name,
            "total": sum([item.quantity * item.price for item in order.items]),
            "order_count": len(order.items)
        } for order in orders]), npartitions=4)
        df_grouped = df.groupby('customer_name').agg({
            'total': 'sum',
            'order_count': 'sum'
        }).compute().reset_index()
        if df_grouped.empty:
            app_logger.warning("No data available for training customer segmentation model")
            return
        X = df_grouped[['total', 'order_count']]
        X_scaled = self.scaler.fit_transform(X)
        self.kmeans_model = KMeans(n_clusters=3, random_state=42)
        self.kmeans_model.fit(X_scaled)
        self.save_model(self.kmeans_model, self.kmeans_model_path)
        app_logger.info("Customer segmentation model trained and saved")

    def segment_customers(self) -> pd.DataFrame:
        """Segments customers using the trained model."""
        if not self.kmeans_model:
            self.train_customer_segmentation_model()
        orders = self.data_service.get_all_sales_orders(limit=10000)
        df = dd.from_pandas(pd.DataFrame([{
            "customer_name": order.customer_name,
            "total": sum([item.quantity * item.price for item in order.items]),
            "order_count": len(order.items)
        } for order in orders]), npartitions=4)
        df_grouped = df.groupby('customer_name').agg({
            'total': 'sum',
            'order_count': 'sum'
        }).compute().reset_index()
        X = df_grouped[['total', 'order_count']]
        X_scaled = self.scaler.transform(X)
        df_grouped['segment'] = self.kmeans_model.predict(X_scaled)
        return df_grouped
