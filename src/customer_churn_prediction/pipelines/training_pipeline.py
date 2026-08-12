import os
import sys
from src.customer_churn_prediction.components.data_ingestion import DataIngestion
from src.customer_churn_prediction.components.data_transformation import DataTransformation
from src.customer_churn_prediction.components.model_tranier import ModelTrainer

class TrainingPipeline:
    def __init__(self):
        pass

    def run_pipeline(self):
        try:
            print("[1/3] Starting Data Ingestion...")
            ingestion = DataIngestion()
            train_path, test_path = ingestion.initiate_data_ingestion()
            print(f"Data Ingestion completed: {train_path}, {test_path}")

            print("[2/3] Starting Data Transformation (including SMOTE)...")
            transformation = DataTransformation()
            X_train, y_train, X_test, y_test, _ = transformation.initiate_data_transformation(train_path, test_path)
            print("Data Transformation completed successfully.")

            print("[3/3] Starting Model Training with MLflow tracking...")
            trainer = ModelTrainer()
            metrics = trainer.initiate_model_trainer(X_train, y_train, X_test, y_test)
            print(f"Model Training completed. Metrics: {metrics}")
            
            return metrics
        except Exception as e:
            raise Exception(f"Pipeline execution failed: {e}")

if __name__ == '__main__':
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
