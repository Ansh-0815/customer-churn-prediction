import json
import os
import subprocess
import sys
import tempfile
import time

from flask import Flask, Response, jsonify, render_template, request

from src.customer_churn_prediction.pipelines.prediction_pipeline import (
    CustomData,
    PredictPipeline,
    validate_payload,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates"),
)

# Vercel (and most serverless platforms) cannot run long background jobs and have
# a read-only filesystem, so in-app retraining is only available on a normal server.
IS_SERVERLESS = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))
TRAIN_LOG_PATH = os.path.join(tempfile.gettempdir(), "churn_training.log")

training_process = None
predict_pipeline = PredictPipeline()

DEFAULT_METRICS = {
    "accuracy": 0.793,
    "precision": 0.638,
    "recall": 0.528,
    "f1": 0.578,
    "roc_auc": 0.843,
}

DEFAULT_IMPORTANCE = [
    ["tenure", 0.178],
    ["Contract_One year", 0.154],
    ["MonthlyCharges", 0.132],
    ["TotalCharges", 0.119],
    ["InternetService_Fiber optic", 0.086],
]


def read_json_file(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            pass
    return default


def get_saved_metrics():
    return read_json_file(os.path.join(BASE_DIR, "models", "metrics.json"), DEFAULT_METRICS)


@app.route("/")
def home():
    raw = get_saved_metrics()
    metrics = {k: raw.get(k, 0) * 100 for k in ("accuracy", "roc_auc", "recall", "precision", "f1")}
    return render_template("index.html", metrics=metrics, training_enabled=not IS_SERVERLESS)


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not data:
        return jsonify({"status": "error", "message": "No JSON data provided"}), 400

    try:
        clean = validate_payload(data)
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    try:
        df = CustomData(**clean).get_data_as_dataframe()
        pred, prob = predict_pipeline.predict(df)
        return jsonify({
            "status": "success",
            "prediction": "Churn" if int(pred) == 1 else "No Churn",
            "churn_probability": round(float(prob), 3),
        })
    except Exception as e:
        app.logger.exception("Prediction failed")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/metrics", methods=["GET"])
def get_metrics_endpoint():
    return jsonify(get_saved_metrics())


@app.route("/feature_importance", methods=["GET"])
def get_feature_importance():
    path = os.path.join(BASE_DIR, "models", "feature_importance.json")
    return jsonify(read_json_file(path, DEFAULT_IMPORTANCE))


@app.route("/train", methods=["POST"])
def train_model():
    global training_process

    if IS_SERVERLESS:
        return jsonify({
            "status": "error",
            "message": "Retraining is disabled on serverless hosting (Vercel). "
                       "Run `python main.py` locally and redeploy the updated models/ folder.",
        }), 501

    try:
        if training_process and training_process.poll() is None:
            return jsonify({"status": "error", "message": "Training pipeline is already running."}), 400

        with open(TRAIN_LOG_PATH, "w", encoding="utf-8") as f:
            f.write("[System] Initializing training pipeline...\n")

        env = os.environ.copy()
        env["PYTHONPATH"] = BASE_DIR + os.pathsep + env.get("PYTHONPATH", "")
        log_file = open(TRAIN_LOG_PATH, "a", buffering=1, encoding="utf-8")
        training_process = subprocess.Popen(
            [sys.executable, "-u", os.path.join(BASE_DIR, "main.py")],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            cwd=BASE_DIR,
        )
        log_file.close()  # the child process keeps its own handle

        return jsonify({"status": "success", "message": "Model training pipeline triggered."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/train/stream", methods=["GET"])
def train_stream():
    def generate():
        if IS_SERVERLESS or not os.path.exists(TRAIN_LOG_PATH):
            yield "data: [System] No training log available.\n\n"
            yield "data: [EOF]\n\n"
            return

        with open(TRAIN_LOG_PATH, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if line:
                    if line.strip():
                        yield f"data: {line.strip()}\n\n"
                    continue
                # No new output: stop once the process has finished (or never started)
                if training_process is None or training_process.poll() is not None:
                    for leftover in f.read().splitlines():
                        if leftover.strip():
                            yield f"data: {leftover.strip()}\n\n"
                    yield "data: [EOF]\n\n"
                    break
                time.sleep(0.5)

    return Response(generate(), mimetype="text/event-stream")


@app.route("/notebook", methods=["GET"])
def get_notebook_html():
    path = os.path.join(BASE_DIR, "templates", "notebook.html")
    if not os.path.exists(path):
        return "Notebook file not found.", 404
    return render_template("notebook.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
