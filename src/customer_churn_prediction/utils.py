import os
import sys
import joblib

# Polyfill module mapping for legacy scikit-learn unpickling in serverless environments
try:
    import sklearn._loss.loss as _sklearn_loss
    sys.modules['loss'] = _sklearn_loss
except Exception:
    pass

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        joblib.dump(obj, file_path)
    except Exception as e:
        raise Exception(f"Error saving object to {file_path}: {e}")

def load_object(file_path):
    try:
        return joblib.load(file_path)
    except Exception as e:
        raise Exception(f"Error loading object from {file_path}: {e}")
