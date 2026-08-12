import os
import sys
import json
import mlflow
import mlflow.sklearn
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from src.customer_churn_prediction.utils import save_object, load_object

class ModelTrainer:
    def __init__(self):
        # Resolve paths dynamically relative to project root
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.model_file_path = os.path.join(self.project_root, "models", "churn_model.pkl")
        self.metrics_file_path = os.path.join(self.project_root, "models", "metrics.json")
        self.columns_file_path = os.path.join(self.project_root, "models", "model_columns.pkl")
        self.feature_importance_file_path = os.path.join(self.project_root, "models", "feature_importance.json")

    def initiate_model_trainer(self, X_train, y_train, X_test, y_test):
        try:
            os.makedirs(os.path.dirname(self.model_file_path), exist_ok=True)
            
            # Gradient Boosting parameters matching the notebook tuning
            params = {
                'n_estimators': 150,
                'max_depth': 4,
                'learning_rate': 0.05,
                'subsample': 0.8,
                'random_state': 42
            }

            # MLflow configuration
            mlflow_db_path = os.path.join(self.project_root, "mlflow.db")
            mlflow.set_tracking_uri(f"sqlite:///{mlflow_db_path}")
            mlflow.set_experiment("Telco_Customer_Churn_Prediction")

            with mlflow.start_run() as run:
                model = GradientBoostingClassifier(**params)
                model.fit(X_train, y_train)

                # Predictions
                y_pred = model.predict(X_test)
                y_prob = model.predict_proba(X_test)[:, 1]

                # Calculate metrics
                metrics = {
                    'accuracy': float(accuracy_score(y_test, y_pred)),
                    'precision': float(precision_score(y_test, y_pred)),
                    'recall': float(recall_score(y_test, y_pred)),
                    'f1': float(f1_score(y_test, y_pred)),
                    'roc_auc': float(roc_auc_score(y_test, y_prob))
                }

                # Log parameters and metrics to MLflow
                mlflow.log_params(params)
                mlflow.log_metrics(metrics)
                mlflow.sklearn.log_model(model, "model")

                # Save model to disk
                save_object(self.model_file_path, model)

                # Save metrics to json file for Flask access
                with open(self.metrics_file_path, 'w') as f:
                    json.dump(metrics, f, indent=2)

                # Extract and save feature importances
                try:
                    columns = load_object(self.columns_file_path)
                    importances = model.feature_importances_.tolist()
                    feat_imp = sorted(zip(columns, importances), key=lambda x: x[1], reverse=True)[:5]
                    with open(self.feature_importance_file_path, 'w') as f:
                        json.dump(feat_imp, f, indent=2)
                except Exception as ex:
                    print(f"Warning: Failed to save feature importances: {ex}")

                return metrics
        except Exception as e:
            raise Exception(f"Model training failed: {e}")
