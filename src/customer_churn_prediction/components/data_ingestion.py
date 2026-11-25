import os

import pandas as pd
from sklearn.model_selection import train_test_split
from src.customer_churn_prediction import config

class DataIngestion:
    def __init__(self):
        self.raw_data_path = config.RAW_DATA_PATH
        self.train_data_path = os.path.join(config.ARTIFACT_DIR, "train.csv")
        self.test_data_path = os.path.join(config.ARTIFACT_DIR, "test.csv")

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
