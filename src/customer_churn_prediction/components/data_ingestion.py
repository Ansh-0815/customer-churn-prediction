import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self):
        # Resolve paths dynamically relative to project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        self.raw_data_path = os.path.join(project_root, "data", "Telco-Customer-Churn.csv")
        self.train_data_path = os.path.join(project_root, "artifacts", "train.csv")
        self.test_data_path = os.path.join(project_root, "artifacts", "test.csv")

    def initiate_data_ingestion(self):
        try:
            df = pd.read_csv(self.raw_data_path)
            
            os.makedirs(os.path.dirname(self.train_data_path), exist_ok=True)
            
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42, stratify=df['Churn'])
            
            train_set.to_csv(self.train_data_path, index=False, header=True)
            test_set.to_csv(self.test_data_path, index=False, header=True)
            
            return self.train_data_path, self.test_data_path
        except Exception as e:
            raise Exception(f"Data ingestion failed: {e}")
