import os
import sys
import types
import joblib

# Comprehensive polyfills for scikit-learn cross-version unpickling on Vercel
try:
    import sklearn._loss.loss as _sklearn_loss
    sys.modules['loss'] = _sklearn_loss
    sys.modules['sklearn._loss'] = sys.modules.get('sklearn._loss', _sklearn_loss)

    class DummyLossModule(types.ModuleType):
        def __getattr__(self, name):
            return getattr(_sklearn_loss, name, object)

    sys.modules['_loss'] = DummyLossModule('_loss')
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
        try:
            with open(file_path, 'rb') as f:
                return joblib.load(f)
        except Exception:
            raise Exception(f"Error loading object from {file_path}: {e}")
