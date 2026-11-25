import os
import numpy as np
import pandas as pd
from src.customer_churn_prediction.utils import load_object

ALLOWED_VALUES = {
    "gender": {"Female", "Male"},
    "Partner": {"Yes", "No"},
    "Dependents": {"Yes", "No"},
    "PhoneService": {"Yes", "No"},
    "MultipleLines": {"Yes", "No", "No phone service"},
    "InternetService": {"DSL", "Fiber optic", "No"},
    "OnlineSecurity": {"Yes", "No", "No internet service"},
    "OnlineBackup": {"Yes", "No", "No internet service"},
    "DeviceProtection": {"Yes", "No", "No internet service"},
    "TechSupport": {"Yes", "No", "No internet service"},
    "StreamingTV": {"Yes", "No", "No internet service"},
    "StreamingMovies": {"Yes", "No", "No internet service"},
    "Contract": {"Month-to-month", "One year", "Two year"},
    "PaperlessBilling": {"Yes", "No"},
    "PaymentMethod": {
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)",
    },
}
NUMERIC_FIELDS = ("SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges")


def validate_payload(data):
    """Validate and normalise a raw request payload. Raises ValueError on bad input."""
    clean = {}
    for field, allowed in ALLOWED_VALUES.items():
        value = data.get(field)
        if value not in allowed:
            raise ValueError(f"Invalid or missing value for '{field}'. Allowed: {sorted(allowed)}")
        clean[field] = value

    for field in NUMERIC_FIELDS:
        try:
            number = float(data.get(field))
        except (TypeError, ValueError):
            raise ValueError(f"'{field}' must be a number")
        if number != number or number in (float("inf"), float("-inf")) or number < 0:
            raise ValueError(f"'{field}' must be a non-negative number")
        clean[field] = number

    if clean["SeniorCitizen"] not in (0.0, 1.0):
        raise ValueError("'SeniorCitizen' must be 0 or 1")
    clean["SeniorCitizen"] = int(clean["SeniorCitizen"])
    return clean


class PredictPipeline:
    def __init__(self):
        # Resolve paths dynamically relative to project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.model_path = os.path.join(project_root, "models", "churn_model.pkl")
        self.preprocessor_path = os.path.join(project_root, "models", "scaler.pkl")
        self.columns_path = os.path.join(project_root, "models", "model_columns.pkl")
        self._artifacts = None

    def _load(self):
        # Load once per process (important for warm serverless invocations)
        if self._artifacts is None:
            self._artifacts = (
                load_object(self.model_path),
                load_object(self.preprocessor_path),
                load_object(self.columns_path),
            )
        return self._artifacts

    def predict(self, features_df):
        try:
            model, scaler, model_columns = self._load()
            features_df = features_df.copy()

            # Categorical vs Numerical matching training columns
            categorical_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                                'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                                'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
                                'PaperlessBilling', 'PaymentMethod']

            # Label encode binary object columns (exactly 2 unique values)
            binary_mappings = {
                'gender': {'Female': 0, 'Male': 1},
                'Partner': {'No': 0, 'Yes': 1},
                'Dependents': {'No': 0, 'Yes': 1},
                'PhoneService': {'No': 0, 'Yes': 1},
                'PaperlessBilling': {'No': 0, 'Yes': 1}
            }
            for col, mapping in binary_mappings.items():
                if col in features_df.columns:
                    features_df[col] = features_df[col].map(mapping)
                    if features_df[col].isnull().any():
                        raise ValueError(f"Unsupported value for '{col}'")

            # Make sure all features are strings or numbers
            features_df['SeniorCitizen'] = features_df['SeniorCitizen'].astype(int)
            features_df['tenure'] = features_df['tenure'].astype(float)
            features_df['MonthlyCharges'] = features_df['MonthlyCharges'].astype(float)
            features_df['TotalCharges'] = features_df['TotalCharges'].astype(float)

            # One-Hot Encoding only on multi-category features
            multi_cols = [c for c in categorical_cols if c not in binary_mappings]
            features_encoded = pd.get_dummies(features_df, columns=multi_cols, drop_first=True)

            # Reindex to match the columns list from training
            features_aligned = features_encoded.reindex(columns=model_columns, fill_value=0)

            # Cast bools to int64
            for col in features_aligned.columns:
                if features_aligned[col].dtype == bool:
                    features_aligned[col] = features_aligned[col].astype(np.int64)

            # Scale features
            scaled_features = scaler.transform(features_aligned)

            # Churn prediction and probability
            preds = model.predict(scaled_features)
            probs = model.predict_proba(scaled_features)[:, 1]

            return preds[0], probs[0]
        except Exception as e:
            raise Exception(f"Prediction failed: {e}")

class CustomData:
    def __init__(self, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
                 MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection,
                 TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling,
                 PaymentMethod, MonthlyCharges, TotalCharges):
        self.gender = gender
        self.SeniorCitizen = SeniorCitizen
        self.Partner = Partner
        self.Dependents = Dependents
        self.tenure = tenure
        self.PhoneService = PhoneService
        self.MultipleLines = MultipleLines
        self.InternetService = InternetService
        self.OnlineSecurity = OnlineSecurity
        self.OnlineBackup = OnlineBackup
        self.DeviceProtection = DeviceProtection
        self.TechSupport = TechSupport
        self.StreamingTV = StreamingTV
        self.StreamingMovies = StreamingMovies
        self.Contract = Contract
        self.PaperlessBilling = PaperlessBilling
        self.PaymentMethod = PaymentMethod
        self.MonthlyCharges = MonthlyCharges
        self.TotalCharges = TotalCharges

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "SeniorCitizen": [self.SeniorCitizen],
                "Partner": [self.Partner],
                "Dependents": [self.Dependents],
                "tenure": [self.tenure],
                "PhoneService": [self.PhoneService],
                "MultipleLines": [self.MultipleLines],
                "InternetService": [self.InternetService],
                "OnlineSecurity": [self.OnlineSecurity],
                "OnlineBackup": [self.OnlineBackup],
                "DeviceProtection": [self.DeviceProtection],
                "TechSupport": [self.TechSupport],
                "StreamingTV": [self.StreamingTV],
                "StreamingMovies": [self.StreamingMovies],
                "Contract": [self.Contract],
                "PaperlessBilling": [self.PaperlessBilling],
                "PaymentMethod": [self.PaymentMethod],
                "MonthlyCharges": [self.MonthlyCharges],
                "TotalCharges": [self.TotalCharges]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise Exception(f"Converting data to dataframe failed: {e}")
