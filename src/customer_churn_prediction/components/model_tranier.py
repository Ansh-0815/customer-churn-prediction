import json
import os

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from src.customer_churn_prediction import config
from src.customer_churn_prediction.utils import save_object, load_object

# MLflow is optional: it is used for local experiment tracking but is not
# installed on serverless deployments (requirements.txt does not include it).
try:
    import mlflow
    import mlflow.sklearn
except ImportError:
    mlflow = None


class ModelTrainer:
    def __init__(self):
        self.project_root = config.PROJECT_ROOT
        self.model_file_path = os.path.join(config.MODEL_DIR, "churn_model.pkl")
        self.metrics_file_path = os.path.join(config.MODEL_DIR, "metrics.json")
        self.columns_file_path = os.path.join(config.MODEL_DIR, "model_columns.pkl")
        self.feature_importance_file_path = os.path.join(config.MODEL_DIR, "feature_importance.json")

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

            model = GradientBoostingClassifier(**params)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]

            metrics = {
                'accuracy': float(accuracy_score(y_test, y_pred)),
                'precision': float(precision_score(y_test, y_pred)),
                'recall': float(recall_score(y_test, y_pred)),
                'f1': float(f1_score(y_test, y_pred)),
                'roc_auc': float(roc_auc_score(y_test, y_prob))
            }

            # Save model, metrics and feature importances first so the web app always
            # gets fresh artifacts, even if experiment tracking fails afterwards
            save_object(self.model_file_path, model)
            with open(self.metrics_file_path, 'w') as f:
                json.dump(metrics, f, indent=2)

            try:
                columns = load_object(self.columns_file_path)
                importances = model.feature_importances_.tolist()
                feat_imp = sorted(zip(columns, importances), key=lambda x: x[1], reverse=True)[:5]
                with open(self.feature_importance_file_path, 'w') as f:
                    json.dump(feat_imp, f, indent=2)
            except Exception as ex:
                print(f"Warning: Failed to save feature importances: {ex}")

            self._log_to_mlflow(model, params, metrics)
            return metrics
        except Exception as e:
            raise Exception(f"Model training failed: {e}")

    def _log_to_mlflow(self, model, params, metrics):
        if mlflow is None or config.IS_SERVERLESS:
            print("MLflow tracking skipped (not available in this environment).")
            return
        try:
            mlflow.set_tracking_uri(f"sqlite:///{os.path.join(self.project_root, 'mlflow.db')}")
            mlflow.set_experiment("Telco_Customer_Churn_Prediction")
            with mlflow.start_run():
                mlflow.log_params(params)
                mlflow.log_metrics(metrics)
                mlflow.sklearn.log_model(model, name="model", serialization_format="cloudpickle")
        except Exception as ex:
            print(f"Warning: MLflow logging failed: {ex}")
