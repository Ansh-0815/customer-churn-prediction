import os
import sys
import pandas as pd

class ModelMonitoring:
    def __init__(self):
        pass

    def run_checks(self, df):
        try:
            checks = {
                "shape": df.shape,
                "null_values": df.isnull().sum().to_dict(),
                "label_distribution": df['Churn'].value_counts().to_dict() if 'Churn' in df.columns else None
            }
            return checks
        except Exception as e:
            raise Exception(f"Model monitoring checks failed: {e}")
