import os
import sys
import pandas as pd
import numpy as np
from src.customer_churn_prediction.utils import load_object

class PredictPipeline:
    def __init__(self):
        # Resolve paths dynamically relative to project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.model_path = os.path.join(project_root, "models", "churn_model.pkl")
        self.preprocessor_path = os.path.join(project_root, "models", "scaler.pkl")
        self.columns_path = os.path.join(project_root, "models", "model_columns.pkl")

    def predict(self, features_df):
        try:
            model = load_object(self.model_path)
            scaler = load_object(self.preprocessor_path)
            model_columns = load_object(self.columns_path)

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
