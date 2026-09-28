import sys
import os

# Polyfill module mapping for legacy scikit-learn unpickling in serverless runtimes
try:
    import sklearn._loss.loss as _sklearn_loss
    sys.modules['loss'] = _sklearn_loss
    sys.modules['sklearn._loss'] = sys.modules.get('sklearn._loss', _sklearn_loss)
except Exception:
    pass

from app import app
