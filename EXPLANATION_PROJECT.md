# Customer Churn Production Project - Architectural Deep Dive

This document explains the production system architecture, directory layout, Django web views, frosted glassmorphism styling, and cloud deployment steps implemented in the project. It is structured to be beginner-friendly, explaining **what** we used, **why** we used it, and **what else** we could have used.

---

## 📌 Directory Structure Overview

```
Customer_Churn_Model/
├── manage.py                   # Django CLI entrypoint
├── Procfile                    # Gunicorn production start command (Linux/Render)
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
```

---

## 1. Django Web views (`churn_app/views.py`)

This file acts as the router. It receives HTTP requests from the browser, runs Python code, and returns templates or JSON.

### A. The Predict Endpoint (`predict`)
- **What it is**: A POST endpoint (`/predict`) that takes JSON customer details, preprocesses them, and returns the churn probability.
- **Why use it**: Allows other applications or the frontend to score customers in real-time.
- **What if we used something else?**: 
  - If we used simple static rule-based checks, we would miss complex non-linear combinations of features.
  - If we didn't align columns, the model would crash if the user omitted a feature in the input payload.

### B. The Retraining Trigger (`train_model`)
- **What it is**: A POST endpoint (`/train`) that triggers the training pipeline in a background process.
- **Why use it**: Spawning it as a background `subprocess.Popen` prevents the HTTP request from timing out or freezing the UI while training occurs.
- **What if we used something else?**: If we executed the training synchronously inside the request loop, the browser would throw a "504 Gateway Timeout" because training takes 1-2 seconds, exceeding default synchronous gateway limits.

### C. Server-Sent Events Log Streaming (`train_stream`)
- **What it is**: A GET endpoint (`/train/stream`) that streams log lines back to the browser console.
- **Why use it**: Lightweight, unidirectional communication using standard HTTP protocols.
- **What if we used WebSockets?**: WebSockets are bidirectional and require extra libraries (like Django Channels) and separate servers (like Redis), which increases server costs and complexity. SSE is built-in and free.

---

## 2. Frosted Glassmorphism Styling (`static/style.css`)

### A. Visual Aesthetics
- **What it is**: Semi-transparent card surfaces combined with a background blur.
  ```css
  background: rgba(255, 255, 255, 0.48);
  backdrop-filter: blur(18px) saturate(190%);
  ```
- **Why use it**: Simulates premium glass plates over a grid canvas, improving visual presentation for interviews and production demos.
- **What if we used Tailwind CSS?**: Tailwind is excellent for standard utility layouts, but custom vanilla CSS provides absolute control over glass shadows, border highlights, and dynamic transitions without adding bulky frameworks.

---

## 3. Production Deployment & Optimizations

### A. Pre-rendered Notebook Caching (RAM Optimization)
- **What it is**: Converting the Jupyter Notebook file to HTML (`templates/notebook.html`) during development, rather than converting it on-the-fly inside the views.
- **Why use it**: Dynamic conversion via `nbconvert` compiles Jinja templates and parses massive JSON structures, peaking memory past 512 MB. Static rendering serves the same content in under 5 milliseconds with **0 MB extra RAM**.
- **What if we didn't do this?**: Render's free tier would throw a **503 Out-of-Memory (OOM)** error or crash the site when visiting `/notebook`.

### B. WhiteNoise Static Asset Compression
- **What it is**: A Python package that sits inside the Django middleware stack to serve static files (CSS, JS, images) directly from the application process.
- **Why use it**: Django by default does not serve static files in production. WhiteNoise compresses files (Gzip/Brotli) and adds far-future caching headers.
- **What if we used Nginx or AWS S3?**: Nginx or S3 are excellent for large-scale enterprise systems, but they add deployment costs and require extra configuration. WhiteNoise is self-contained and free.
