# Customer Churn Production Project - Architectural Deep Dive

This document explains the production system architecture, components, pipeline code, Django web application views, frosted glassmorphism styling, and cloud deployment steps implemented in the project.

---

## 📌 Directory Structure Overview

```
Customer_Churn_Model/
├── manage.py                   # Django CLI entrypoint
├── Procfile                    # Gunicorn production start command (Gunicorn)
├── render.yaml                 # Render cloud blueprint config (1-click deploy)
├── requirements.txt            # Python pinned packages
│
├── churn_project/              # Django core configuration folder
│   ├── settings.py             # Settings (WhiteNoise, database, middleware, static files)
│   ├── urls.py                 # Root router routing to churn_app
│   └── wsgi.py                 # Web Server Gateway Interface for production
│
├── churn_app/                  # Django Web Application Folder
│   ├── urls.py                 # Route definitions (/, /predict, /train, /train/stream, /notebook)
│   └── views.py                # Views handling scoring APIs, SSE streaming, and precompiled notebooks
│
├── src/                        # Machine Learning Pipeline Source Code
│   └── customer_churn_prediction/
│       ├── components/         # Pipeline Components (Data Ingestion, Transformation, Model Trainer)
│       │   ├── data_ingestion.py
│       │   ├── data_transformation.py
│       │   └── model_tranier.py
│       └── pipelines/          # Training & Prediction Pipelines
│           ├── training_pipeline.py
│           └── prediction_pipeline.py
│
├── templates/
│   ├── index.html              # Frosted glassmorphism Bento dashboard template
│   └── notebook.html           # Pre-compiled static notebook HTML template (memory optimized)
│
├── static/
│   ├── style.css               # CSS file defining the Ultra Frosted Glassmorphism theme
│   ├── script.js               # JavaScript handling Chart.js plots, SSE log streaming, & prediction forms
│   └── assets/                 # Live site screenshots & notebook study charts
│
├── models/
│   ├── churn_model.pkl         # Serialized Gradient Boosting weights
│   ├── scaler.pkl              # Scaler object mapping input fields to training scale
│   ├── model_columns.pkl       # Training column alignment list
│   └── metrics.json            # Model validation metrics
```

---

## 1. Machine Learning Pipelines (under `src/`)

### A. Data Ingestion (`data_ingestion.py`)
- **Action**: Reads `data/Telco-Customer-Churn.csv`, splits it into 80% training and 20% testing splits (`train.csv` & `test.csv`), and saves them into the local directory.
- **Why**: Standardizes data separation from the beginning, ensuring the model never sees test data before preprocessing.

### B. Data Transformation & SMOTE (`data_transformation.py`)
- **Action**:
  - Imputes missing `TotalCharges` strings using medians.
  - Encodes binary features (gender, partner, etc.) to 0/1.
  - Multi-category variables are one-hot encoded using dummy variables.
  - Aligns train and test column headers to prevent mismatch issues.
  - Fits and applies `StandardScaler` to scale columns to uniform variance.
  - Applies **SMOTE** to balance the training set churn representations.
  - Saves the resulting `scaler.pkl` and `model_columns.pkl` for the prediction engine.
- **Why**: SMOTE balances target class representation, boosting churn **Recall by +23.5%**.

### C. Model Training & MLflow (`model_tranier.py`)
- **Action**:
  - Sets MLflow experiment tracking URI to `sqlite:///mlflow.db`.
  - Configures tuned hyperparameters matching the notebook randomized search results.
  - Fits a `GradientBoostingClassifier` model.
  - Logs parameters, accuracy, recall, precision, F1, and ROC AUC metrics to MLflow.
  - Serializes model weights to `models/churn_model.pkl`.
  - Saves model metrics to `models/metrics.json` and top 5 feature importances to `models/feature_importance.json`.
- **Why**: Automates model lineage tracking and model versioning.

---

## 2. Django Production Web Server (`churn_app/views.py`)

Handles all Web requests, JSON API endpoints, background retraining processes, and Server-Sent Events (SSE):

1. **`home(request)`**:
   - Loads `models/metrics.json`. If it doesn't exist, loads baseline fallback metrics. Renders `index.html` with metrics passed to the template context.
2. **`predict(request)`**:
   - REST API endpoint (`POST /predict`). Accepts JSON containing customer details.
   - Formats input into a pandas DataFrame, transforms features using `scaler.pkl`, aligns columns using `model_columns.pkl`, runs model inference using `churn_model.pkl`, and returns predicted label and probability.
3. **`train_model(request)`**:
   - REST API (`POST /train`).
   - Spawns a background process running `sys.executable main.py` using Python's `subprocess.Popen` and redirects stdout/stderr to `models/training.log`.
   - Returns a success response immediately so the web server doesn't freeze or block during execution.
4. **`train_stream(request)`**:
   - SSE endpoint (`GET /train/stream`).
   - Uses Django's `StreamingHttpResponse` to yield log file updates.
   - Streams log lines line-by-line in real time, appending `data: ` prefixes, ending with `data: [EOF]` when the retraining subprocess exits.
5. **`get_notebook_html(request)`**:
   - Renders the pre-compiled Jupyter Notebook HTML template [`templates/notebook.html`](file:///c:/Users/agarw/Desktop/Customer_Churn_Model/templates/notebook.html).
   - If not compiled, dynamically parses `churn_prediction.ipynb` using `nbconvert` and returns the HTML.

---

## 3. Frosted Glassmorphism Design System (`style.css` & `script.js`)

- **Design System Tokens (`style.css`)**:
  - Background Canvas: Solid slate-grey (`#cbd5e1`) with a flat 2D vector grid mesh (`rgba(15, 23, 42, 0.22)`) and upper radial glow vignette.
  - Glass Bento Cards & Sidebar: Translucent white overlays (`rgba(255, 255, 255, 0.48)`) with `backdrop-filter: blur(18px) saturate(190%)` and inset specular highlights (`box-shadow: inset 0 1.5px 1px 0 rgba(255, 255, 255, 0.9)`).
  - Typography: Crisp dark slate (`#0f172a` & `#334155`) for readable text over translucent cards.
- **Dynamic Frontend Features (`script.js`)**:
  - **Dynamic Tab Routing**: Swapping active tab wrappers (`#overview-tab`, `#predict-tab`, `#training-tab`, `#eda-tab`) and updating the sidebar highlight state.
  - **Auto-Fill Sample Data**: Fills predictor form variables instantly with sample profiles representing high-risk or low-risk profiles (`loadSampleData('churn')` and `loadSampleData('loyal')`).
  - **SSE Live Terminal**: Listens to `/train/stream` using JavaScript's `EventSource`, auto-scrolls, and outputs lines directly into the web terminal console.
  - **Circular SVG Risk Gauge**: Dynamically animates the circular path fill (`stroke-dasharray`) and updates gauge color coding based on predicted risk (Safe/Warning/Danger).

---

## 4. Production Optimizations & Deployment

### A. Pre-rendered Notebook Caching (RAM Optimization)
- **Problem**: Rendering a heavy `.ipynb` file using `nbconvert` dynamically on every request to `/notebook` exceeds 512 MB memory on free cloud tiers, causing Gunicorn timeout errors.
- **Solution**: Pre-compiling `churn_prediction.ipynb` to `templates/notebook.html` once during building. Serve it statically using Django's rendering engine in **<5 milliseconds** with **0 MB extra RAM**.

### B. WhiteNoise Static File Compression
- **Setup**: `whitenoise.middleware.WhiteNoiseMiddleware` configured right after `SecurityMiddleware`.
- **Storage**: `whitenoise.storage.CompressedManifestStaticFilesStorage` handles manifest generation, Gzip compression, and long-term caching headers for static assets.

### C. Cloud Deploy Configuration (Render)
- **Procfile**: `web: gunicorn churn_project.wsgi:application` routes production traffic to the Django WSGI application.
- **render.yaml Blueprint**: Configures environment variables, generates a secure `SECRET_KEY`, sets `DEBUG=False`, runs `pip install`, compiles static files, runs migrations, and spawns Gunicorn.
