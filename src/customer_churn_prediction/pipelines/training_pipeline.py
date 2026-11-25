from src.customer_churn_prediction.components.data_ingestion import DataIngestion
from src.customer_churn_prediction.components.data_transformation import DataTransformation
from src.customer_churn_prediction.components.model_tranier import ModelTrainer


class TrainingPipeline:
    def __init__(self, log=print):
        self.log = log

    def run_pipeline(self):
        try:
            self.log("[1/3] Starting Data Ingestion...")
            train_path, test_path = DataIngestion().initiate_data_ingestion()
            self.log("Data Ingestion completed.")

            self.log("[2/3] Starting Data Transformation (including SMOTE)...")
            X_train, y_train, X_test, y_test, _ = DataTransformation().initiate_data_transformation(
                train_path, test_path
            )
            self.log("Data Transformation completed successfully.")

            self.log("[3/3] Starting Model Training...")
            metrics = ModelTrainer().initiate_model_trainer(X_train, y_train, X_test, y_test)
            self.log(f"Model Training completed. Metrics: {metrics}")

            return metrics
        except Exception as e:
            raise Exception(f"Pipeline execution failed: {e}")


if __name__ == '__main__':
    TrainingPipeline().run_pipeline()
