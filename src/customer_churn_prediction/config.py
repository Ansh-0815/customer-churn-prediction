import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Serverless platforms (Vercel, AWS Lambda) have a read-only filesystem except /tmp
IS_SERVERLESS = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))

RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "Telco-Customer-Churn.csv")

# Models shipped with the repository (read-only on Vercel)
BUNDLED_MODEL_DIR = os.path.join(PROJECT_ROOT, "models")

# Where training writes its output. On serverless this is a temporary folder, so a
# retrained model lives only as long as the warm function instance.
if IS_SERVERLESS:
    MODEL_DIR = os.path.join("/tmp", "churn_models")
    ARTIFACT_DIR = os.path.join("/tmp", "churn_artifacts")
else:
    MODEL_DIR = BUNDLED_MODEL_DIR
    ARTIFACT_DIR = os.path.join(PROJECT_ROOT, "artifacts")


def resolve_model_file(name):
    """Prefer a freshly trained file in MODEL_DIR, fall back to the bundled one."""
    fresh = os.path.join(MODEL_DIR, name)
    return fresh if os.path.exists(fresh) else os.path.join(BUNDLED_MODEL_DIR, name)
