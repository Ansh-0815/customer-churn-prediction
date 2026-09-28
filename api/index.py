import sys
import os

# Polyfill module mapping for legacy scikit-learn unpickling in serverless runtimes
try:
    import sklearn._loss.loss as _sklearn_loss
    sys.modules['loss'] = _sklearn_loss
except ImportError:
    pass

from app import app
