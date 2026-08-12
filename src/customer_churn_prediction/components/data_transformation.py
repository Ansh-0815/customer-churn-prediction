import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from src.customer_churn_prediction.utils import save_object

class DataTransformation:
    def __init__(self):
        # Resolve paths dynamically relative to project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.preprocessor_obj_file_path = os.path.join(project_root, "models", "scaler.pkl")
        self.columns_obj_file_path = os.path.join(project_root, "models", "model_columns.pkl")

    def clean_data(self, df):
        try:
            df = df.copy()
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())
            
            if 'customerID' in df.columns:
                df = df.drop(columns=['customerID'])
                
            return df
        except Exception as e:
            raise Exception(f"Cleaning data failed: {e}")

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            train_df = self.clean_data(train_df)
            test_df = self.clean_data(test_df)

            target_column = 'Churn'
            
            # Map target Churn to binary integers
            train_df[target_column] = train_df[target_column].map({'Yes': 1, 'No': 0})
            test_df[target_column] = test_df[target_column].map({'Yes': 1, 'No': 0})

            X_train = train_df.drop(columns=[target_column])
            y_train = train_df[target_column]
            X_test = test_df.drop(columns=[target_column])
            y_test = test_df[target_column]

            # Categorical vs Numerical
            categorical_cols = X_train.select_dtypes(include=['object']).columns.tolist()

            # Label encode binary object columns (exactly 2 unique values)
            binary_mappings = {
                'gender': {'Female': 0, 'Male': 1},
                'Partner': {'No': 0, 'Yes': 1},
                'Dependents': {'No': 0, 'Yes': 1},
                'PhoneService': {'No': 0, 'Yes': 1},
                'PaperlessBilling': {'No': 0, 'Yes': 1}
            }
            for col, mapping in binary_mappings.items():
                if col in X_train.columns:
                    X_train[col] = X_train[col].map(mapping)
                    X_test[col] = X_test[col].map(mapping)

            # One-Hot Encoding only on multi-category features
            multi_cols = [c for c in categorical_cols if c not in binary_mappings]
            X_train_encoded = pd.get_dummies(X_train, columns=multi_cols, drop_first=True)
            X_test_encoded = pd.get_dummies(X_test, columns=multi_cols, drop_first=True)

            # Align columns
            X_train_encoded, X_test_encoded = X_train_encoded.align(X_test_encoded, join='left', axis=1, fill_value=0)

            # Ensure all boolean columns are cast to int64/float64 to avoid type issues in MLflow/Sklearn
            for col in X_train_encoded.columns:
                if X_train_encoded[col].dtype == bool:
                    X_train_encoded[col] = X_train_encoded[col].astype(np.int64)
                    X_test_encoded[col] = X_test_encoded[col].astype(np.int64)

            # Feature Scaling
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train_encoded)
            X_test_scaled = scaler.transform(X_test_encoded)

            # Balance target classes with SMOTE
            smote = SMOTE(random_state=42)
            X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)

            # Save scaler and columns list
            save_object(self.preprocessor_obj_file_path, scaler)
            save_object(self.columns_obj_file_path, X_train_encoded.columns.tolist())

            return X_train_res, y_train_res, X_test_scaled, y_test, self.preprocessor_obj_file_path
        except Exception as e:
            raise Exception(f"Data transformation failed: {e}")
