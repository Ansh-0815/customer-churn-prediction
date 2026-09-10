# Customer Churn Prediction - Production Flask Dashboard

[![Framework: Flask](https://img.shields.io/badge/Framework-Flask_3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Deployment: Vercel](https://img.shields.io/badge/Deployment-Vercel_Serverless-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Ansh--0815%2Fcustomer--churn--prediction-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ansh-0815/customer-churn-prediction)

An end-to-end Machine Learning & Web Production System built with **Flask**, **Vercel Serverless**, **MLflow**, and **Scikit-Learn** that predicts telecom customer churn in real time and provides an executive intelligence dashboard with automated retraining and an extended EDA notebook study.

---

## Application Screenshots (Captured from Web Dashboard)

### 1. Executive Churn Dashboard (`/`)
![Executive Churn Dashboard Overview](static/assets/dashboard_overview.png)

### 2. Customer Churn Predictor (`/predict`)
![Customer Churn Predictor Interface](static/assets/churn_predictor.png)

### 3. MLflow Model Retraining & SSE Log Streaming (`/train`)
![MLflow Model Retraining Console](static/assets/model_training.png)

### 4. Extended Exploratory Data Analysis & Feature Exploration (`/eda`)
![Exploratory Data Analysis Dashboard](static/assets/eda_analysis.png)

---

## Extended Exploratory Data Analysis & Notebook Charts

Extracted directly from [`notebook/churn_prediction.ipynb`](notebook/churn_prediction.ipynb):

| Chart 1: Churn Class Distribution | Chart 2: Churn by Contract Type |
| :---: | :---: |
| ![Target Churn Class Distribution](static/assets/notebook_chart_1.png) | ![Churn Rate by Contract Type](static/assets/notebook_chart_2.png) |

| Chart 3: Tenure Cohort Distribution | Chart 4: Monthly Charges vs Churn |
| :---: | :---: |
| ![Tenure vs Churn Distribution](static/assets/notebook_chart_3.png) | ![Monthly Charges vs Churn Distribution](static/assets/notebook_chart_4.png) |

| Chart 5: Internet Service Churn | Chart 6: 10-Model Benchmark |
| :---: | :---: |
| ![Internet Service Type vs Churn](static/assets/notebook_chart_5.png) | ![10-Model Classification Performance Comparison](static/assets/notebook_chart_6.png) |

| Chart 7: Effect of SMOTE | Chart 8: Top Churn Drivers |
| :---: | :---: |
| ![SMOTE Class Imbalance Treatment Effect](static/assets/notebook_chart_7.png) | ![Feature Importance Rankings](static/assets/notebook_chart_8.png) |

---

## Executive Summary

- **Flask Microservices Architecture**: Built with Flask, featuring ultra-fast response times, lightweight serverless architecture for Vercel deployment, semi-transparent frosted acrylic surfaces (`backdrop-filter: blur(18px) saturate(190%)`), inset glass highlights, flat 2D vector grid canvas, and real-time risk scoring.
- **Vercel Zero Cold-Start Deployment**: Configured via `vercel.json` (`@vercel/python`) for instant serverless execution without Render spin-up delays.
- **Extended EDA Analysis & Correlation Matrix**: Features a Pearson feature correlation heatmap matrix, 10-model benchmark comparison table, SMOTE oversampling treatment matrix, and service security stickiness analytics.
- **Instant Risk Predictor**: Form-driven REST API (`/predict`) providing instant single-customer churn risk scoring and circular SVG risk-meter visualization.
- **Live Retraining & SSE Telemetry**: Trigger model retraining directly from the UI (`/train`) with real-time console log streaming via Server-Sent Events (`/train/stream`).
- **Embedded Jupyter Notebook Study**: Renders the project's exploratory data analysis and model comparison notebook (`notebook/churn_prediction.ipynb`) into static HTML (`/notebook`).
- **ML Model Performance**: Evaluated 10 classification algorithms; tuned **Gradient Boosting Classifier** with **SMOTE** oversampling to achieve high recall on churners while maintaining **ROC AUC ≈ 0.84**.

---

## Architecture & Project Structure

```
customer-churn-prediction/
├── app.py                      # Core Flask Application & Serverless Web Handler
├── vercel.json                 # Vercel deployment blueprint & Python builder routing
├── Procfile                    # Production Gunicorn entrypoint
├── requirements.txt            # Python dependencies (Flask, MLflow, Scikit-Learn)
├── README.md                   # Project documentation
│
├── src/                        # Modular Machine Learning Pipeline Engine
│   └── customer_churn_prediction/
│       ├── __init__.py
│       ├── utils.py            # Utility functions (save/load pickle objects)
│       ├── components/         # Pipeline Components
│       │   ├── data_ingestion.py        # Loads raw CSV & splits train/test data
│       │   ├── data_transformation.py   # Median imputation, One-Hot Encoding, StandardScaler, SMOTE
│       │   └── model_tranier.py         # Fits tuned Gradient Boosting & logs to MLflow
│       └── pipelines/          # Execution & Inference Pipelines
│           ├── training_pipeline.py     # End-to-end retraining pipeline executor
│           └── prediction_pipeline.py   # CustomData & PredictPipeline for API scoring
│
├── data/                       # Dataset Storage
│   └── Telco-Customer-Churn.csv # IBM Telco 7,043 Customer Records
│
├── models/                     # Trained Artifacts & Telemetry
│   ├── churn_model.pkl         # Serialized Gradient Boosting Model
│   ├── scaler.pkl              # Serialized StandardScaler Instance
│   ├── model_columns.pkl       # Feature Matrix Column Alignment List
│   ├── metrics.json            # Model Evaluation Metrics JSON Log
│   └── feature_importance.json # Gini Feature Importance Rankings
│
├── templates/                  # Jinja2 HTML Templates
│   ├── index.html              # Frosted Glassmorphism Bento Dashboard
│   └── notebook.html           # Pre-rendered Static Notebook Template
│
├── static/                     # CSS, JS & Image Assets
│   ├── style.css               # Design System Stylesheet
│   ├── script.js               # Client-Side Dynamic Routing & Chart Engine
│   └── assets/                 # Screenshots & Dashboard Charts
│
└── notebook/                   # Research & Exploratory Analysis
    └── churn_prediction.ipynb  # Comprehensive Jupyter Notebook Analysis
```

---

## Deploying to Vercel (1-Click Steps)

1. **Install Vercel CLI** (or connect your GitHub repository on Vercel Dashboard):
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel --prod
   ```
   Vercel automatically detects `vercel.json`, installs dependencies from `requirements.txt`, and serves `app.py` via `@vercel/python`.

---

## Running Locally

1. **Activate Virtual Environment**:
   ```bash
   .\venv\Scripts\activate
   ```

2. **Start Local Flask Server**:
   ```bash
   python app.py
   ```

3. Open **[http://localhost:5000](http://localhost:5000)** in your browser.
