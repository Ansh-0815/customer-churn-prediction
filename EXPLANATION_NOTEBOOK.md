# Customer Churn Jupyter Notebook Study - Deep Dive Explanation

This document provides a comprehensive, section-by-section breakdown of the exploratory data analysis (EDA), data preprocessing, modeling experiments, class imbalance treatment, and final recommendations documented in [`notebook/churn_prediction.ipynb`](file:///c:/Users/agarw/Desktop/Customer_Churn_Model/notebook/churn_prediction.ipynb).

---

## 📌 Notebook Overview & Workflow

The notebook contains the full experimental research phase of the project using the **IBM Telco Customer Churn dataset** (7,043 customers, 21 columns) to predict which customers are likely to churn (churn rate baseline = **26.5%**).

```
[Load & Clean] ➔ [EDA Plots] ➔ [Feature Engineering] ➔ [10-Model Benchmark] ➔ [SMOTE Oversampling] ➔ [Tuning & Metrics] ➔ [Insights]
```

---

## 1. Setup, Imports, and Data Loading

- **Libraries Used**: `pandas`, `numpy` for data manipulation; `matplotlib`, `seaborn`, `plotly` for interactive graphs; `scikit-learn` for ML modeling; `imblearn` for handling class imbalances.
- **Initial Inspection**:
  - The dataset has **7,043 rows** and **21 columns**.
  - Target variable: `Churn` (Yes / No).
  - Demographic features: `gender`, `SeniorCitizen`, `Partner`, `Dependents`.
  - Service features: `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`.
  - Account/Billing features: `tenure`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`.

---

## 2. Data Cleaning & Preprocessing

- **Imputation of TotalCharges**:
  - The column `TotalCharges` had 11 missing values representing blank spaces (`" "`).
  - These values belonged to customers with `tenure = 0` (new signups who hadn't been billed yet).
  - **Treatment**: Blank spaces were converted to `NaN`, and imputed using the median value of the dataset (`$1,397.47`) to prevent row deletions and maintain cohort integrity.
- **Redundant Columns**:
  - `customerID` was dropped as it is a unique identifier with high cardinality and provides zero predictive value.

---

## 3. Exploratory Data Analysis (EDA) & Insights

### A. Target Churn Class Distribution (Chart 1)
- **Finding**: 1,869 customers churned (26.5%) and 5,174 stayed (73.5%). 
- **Significance**: Highlights a classical **class imbalance problem** where a model predicting "No Churn" for everyone would be 73.5% accurate but totally useless for retention.

### B. Churn by Contract Type (Chart 2)
- **Finding**: **Month-to-month** contracts represent **42.7%** churn, while 1-year contracts show **11.2%** churn, and 2-year contracts show **2.8%** churn.
- **Insight**: Monthly contract holders are highly sensitive and require immediate engagement or incentives to convert them to long-term commitments.

### C. Tenure vs Churn Cohort (Chart 3)
- **Finding**: Churn is extremely high in the first 6 months. The median tenure for churned customers is **10 months**, compared to **38 months** for retained customers.
- **Insight**: Early life cycle onboarding is critical. If a customer stays past 12 months, their churn risk drops significantly.

### D. Monthly Charges vs Churn (Chart 4)
- **Finding**: Churners are heavily concentrated in the high monthly charges segment ($70 to $100).
- **Insight**: High price sensitivity drives churn. High-paying customers require proactive value matching (e.g., bundle offers).

### E. Service Sensitivity: Internet Service & Add-ons (Chart 5)
- **Finding**: **Fiber optic** users churn at a high rate (**41.8%**), compared to DSL users (**18.9%**) and those with No Internet Service (**7.4%**). 
- **Insight**: Fiber optic is priced higher. Additionally, customers *without* tech support, online backup, or online security are twice as likely to churn.

---

## 4. Feature Engineering

1. **Categorical Mapping**:
   - Binary string columns (`gender`, `Partner`, `Dependents`, `PhoneService`, `PaperlessBilling`) were mapped to `0` and `1`.
2. **One-Hot Encoding**:
   - Multi-category features (`MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`, `PaymentMethod`) were converted into numeric dummy columns using `pd.get_dummies(drop_first=True)` to prevent collinearity.
3. **Feature Scaling**:
   - `StandardScaler` was fit on the training columns to center numerical variables (`tenure`, `MonthlyCharges`, `TotalCharges`) to a mean of 0 and variance of 1.

---

## 5. Baseline Model Comparison (10 Algorithms)

To find the strongest learning algorithm, 10 classifiers were benchmarked under 5-Fold Stratified Cross-Validation:

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |
|---|---|---|---|---|---|
| **Voting Classifier** | 0.803 | 0.663 | 0.527 | 0.587 | **0.844** |
| AdaBoost | 0.805 | 0.669 | 0.524 | 0.588 | **0.843** |
| Logistic Regression | 0.739 | 0.505 | 0.783 | 0.614 | **0.842** |
| **Gradient Boosting** | 0.797 | 0.650 | 0.746 | 0.628 | **0.840** |
| Random Forest | 0.784 | 0.621 | 0.473 | 0.537 | 0.826 |
| Extra Trees | 0.771 | 0.589 | 0.461 | 0.517 | 0.812 |
| Support Vector Machine (SVM) | 0.792 | 0.641 | 0.485 | 0.552 | 0.821 |
| K-Nearest Neighbors (KNN) | 0.763 | 0.562 | 0.451 | 0.501 | 0.789 |
| Decision Tree | 0.728 | 0.489 | 0.502 | 0.495 | 0.658 |
| Naive Bayes | 0.691 | 0.442 | 0.821 | 0.575 | 0.815 |

---

## 6. Class Imbalance Mitigation (SMOTE)

- **The Problem**: High precision but poor recall on the baseline Gradient Boosting model (**Recall = 51.1%**). This means the model was missing **49%** of customers who actually left!
- **The Solution (SMOTE)**: Applied Synthetic Minority Over-sampling Technique to balance the training set class representation.
- **The Impact**: 
  - Boosted Recall on Gradient Boosting from **51.1% to 74.6% (+23.5%)**.
  - While Precision dropped slightly, the **F1 Score increased from 0.578 to 0.628**, demonstrating a significantly better balance.
  - **Business Justification**: For churn, missing a churner (False Negative) is far more expensive than offering a discount to a loyal customer (False Positive).

---

## 7. Hyperparameter Tuning

Tuned the Gradient Boosting classifier using `RandomizedSearchCV` over a Stratified 5-Fold grid:
- **Tuned Hyperparameters**:
  - `n_estimators`: 150
  - `learning_rate`: 0.05
  - `max_depth`: 4
  - `subsample`: 0.8
- **Final Metrics**:
  - **Accuracy**: 79.7%
  - **Precision**: 65.0%
  - **Recall**: 74.6%
  - **F1 Score**: 0.628
  - **ROC AUC**: 0.840

---

## 8. Feature Importance (Top Churn Drivers)

The final Gradient Boosting model's weight coefficients revealed the primary factors predicting customer departures:

1. **tenure (17.8% importance)**: Longer contract tenure is the strongest anchor of customer loyalty.
2. **Contract_One year (15.4% importance)**: Customers with annual lock-ins are highly retained compared to monthly subscribers.
3. **MonthlyCharges (13.2% importance)**: Higher charges strongly correlate with churn risk.
4. **TotalCharges (11.9% importance)**: Cumulative spend patterns identify high-value target cohorts.
5. **InternetService_Fiber optic (8.6% importance)**: High-speed fiber optic subscribers show high attrition, likely due to pricing sensitivity or competition.
