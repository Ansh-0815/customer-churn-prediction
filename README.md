# Customer Churn Prediction

End-to-end machine learning project that predicts which telecom customers are likely to churn, so the business can act before they leave - built and cleaned up from scratch after reviewing two reference implementations for common bugs and best practices (see [Notes on Reference Notebooks](#notes-on-reference-notebooks) below).

## Executive Summary

- Compared **10 classification algorithms** on churn prediction using Accuracy, Precision, Recall, F1, F2, and ROC AUC.
- **Gradient Boosting, AdaBoost, and Logistic Regression** were the strongest baseline models (ROC AUC ≈ 0.84, confirmed with 5-fold cross-validation).
- Applied **SMOTE** to address class imbalance (26.5% churn rate), trading some precision for a large recall gain - the right tradeoff when missing a churner is costlier than a false alarm.
- Tuned Gradient Boosting with **RandomizedSearchCV** (5-fold CV, ROC AUC scoring) and extracted feature importances to identify the top churn drivers: **tenure, contract type, and monthly/total charges**.
- Saved the final model with `joblib` and built a **correct** single-customer prediction function - including a fix for a subtle but common encoding bug (see below).

## Dataset

**Source:** [IBM Telco Customer Churn dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) - 7,043 customers, 21 features (demographics, account info, subscribed services, and the `Churn` target).

## Project Structure

```
customer-churn-prediction/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── Telco-Customer-Churn.csv
├── notebook/
│   └── churn_prediction.ipynb
└── models/
    ├── churn_model.pkl        # Final tuned Gradient Boosting model
    ├── scaler.pkl              # StandardScaler fit on training data only
    └── model_columns.pkl       # Exact training feature column order
```

## How to Run

```bash
git clone <this-repo-url>
cd customer-churn-prediction
pip install -r requirements.txt
jupyter notebook notebook/churn_prediction.ipynb
```

The notebook runs top-to-bottom with no manual steps - it reads `data/Telco-Customer-Churn.csv`, trains all models, and re-saves the model artifacts into `models/`.

## Methodology

1. **Data Cleaning** - `TotalCharges` is stored as text with 11 blank entries (all customers with `tenure == 0`, i.e. brand-new accounts); converted to numeric and imputed with the median rather than silently dropped.
2. **EDA** - Interactive Plotly charts + seaborn plots covering churn rate, contract type, tenure, monthly charges, internet service, and add-on services (Online Security, Tech Support).
3. **Feature Engineering** - Binary categoricals label-encoded, multi-category categoricals one-hot encoded. Train/test split happens **before** scaling, and the `StandardScaler` is fit only on the training set to avoid data leakage.
4. **Baseline Comparison** - 10 classifiers evaluated on Accuracy/Precision/Recall/F1/F2/ROC AUC, cross-validated for stability.
5. **Class Imbalance Handling** - SMOTE applied to the training set only (never to the test set), compared against class-weighted baselines.
6. **Hyperparameter Tuning** - `RandomizedSearchCV` on Gradient Boosting (25 iterations, 5-fold CV, ROC AUC scoring).
7. **Feature Importance** - Extracted from the tuned model to identify actionable churn drivers.
8. **Model Persistence** - `joblib`-saved model, scaler, and column schema, plus a single-customer prediction function.

## Key Results

### Baseline model comparison (test set)

| Model | Accuracy | Precision | Recall | F1 | ROC AUC |
|---|---|---|---|---|---|
| Voting Classifier | 0.803 | 0.663 | 0.527 | 0.587 | 0.844 |
| AdaBoost | 0.805 | 0.669 | 0.524 | 0.588 | 0.843 |
| Logistic Regression | 0.739 | 0.505 | 0.783 | 0.614 | 0.842 |
| Gradient Boosting | 0.797 | 0.650 | 0.511 | 0.572 | 0.840 |
| Random Forest | 0.784 | 0.621 | 0.473 | 0.537 | 0.826 |

*(Full 10-model table, confusion matrices, and ROC curves are in the notebook.)*

5-fold cross-validation confirmed the ranking is stable (Voting Classifier: 0.850 ± 0.025 ROC AUC; AdaBoost: 0.847 ± 0.026; Logistic Regression: 0.846 ± 0.025).

### Effect of SMOTE

| Model | Recall (baseline) | Recall (SMOTE) |
|---|---|---|
| Logistic Regression | 0.783 | 0.701 |
| Gradient Boosting | 0.511 | 0.746 |
| Random Forest | 0.473 | 0.636 |

Gradient Boosting benefits the most from SMOTE - recall on churners jumps from 51% to 75%, at some cost to precision. This is a good trade for most subscription businesses, where a missed churner is more expensive than an unnecessary retention offer.

### Tuned model (final)

- **Best params:** `learning_rate≈0.089, max_depth=5, n_estimators=369, subsample≈0.92`
- **Cross-validated ROC AUC:** 0.911 (on SMOTE-balanced training data)
- **Test set:** Precision 0.54 / Recall 0.63 / F1 0.58 for the churn class; ROC AUC 0.808

### Top churn drivers (feature importance)

1. **Tenure**
2. **Two-year contract** (protective - reduces churn)
3. **Monthly Charges**
4. **Total Charges**
5. **One-year contract** (also protective)
6. **Electronic check payment method**
7. **Fiber optic internet**

## Business Recommendations

- Target **month-to-month customers in their first 3 months** with onboarding incentives or discounted upgrades to longer contracts.
- Bundle **Online Security and Tech Support** into introductory packages - customers without these add-ons churn noticeably more.
- Review **Fiber optic pricing/reliability** - this segment shows disproportionately high churn versus DSL.
- Use the model's **churn probability score** to prioritize retention outreach rather than contacting the entire customer base.

## Notes on Reference Notebooks

This project was built after reviewing two public reference notebooks on the same dataset, specifically to avoid two real bugs found in them:

1. **Test-set leakage in scaling** - one reference fit a fresh `StandardScaler` on the test set instead of reusing the scaler fit on the training set. Fixed here by always fitting on train only.
2. **Broken single-row inference** - a reference notebook's prediction function used `pd.get_dummies()` directly on a single new customer row. With only one row, every categorical column has just one unique value, so `drop_first=True` treats it as "the first category" and drops it - silently zeroing out every one-hot feature. This project's `predict_churn()` function instead encodes new rows against the **fixed training-time vocabulary** (`model_columns.pkl`), which is the correct approach for production inference.

## Limitations & Future Work

- No temporal/behavioral data (usage trends, support tickets, complaints) - only a single snapshot per customer.
- Customer Lifetime Value (CLV) was not incorporated into retention prioritization.
- Decision threshold was left at the default 0.5; a business-cost-weighted threshold would likely improve real-world ROI.
- A survival analysis (e.g., Kaplan-Meier or Cox proportional hazards) could add a *time-to-churn* dimension a classifier alone can't provide.

## Tech Stack

- **Python:** pandas, numpy, scikit-learn, imbalanced-learn, scipy
- **Visualization:** matplotlib, seaborn, plotly
- **Environment:** Jupyter Notebook

