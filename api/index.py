import os
import sys

# Make the project root importable when running as a Vercel serverless function
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app  # noqa: E402,F401
