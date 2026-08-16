# Customer Churn Jupyter Notebook Study - Deep Dive Explanation

This document explains the exploratory data analysis (EDA), data cleaning, feature scaling, imbalance handling (SMOTE), and model comparisons documented in [`notebook/churn_prediction.ipynb`](file:///c:/Users/agarw/Desktop/Customer_Churn_Model/notebook/churn_prediction.ipynb). It is structured to be beginner-friendly.

---

## 📌 Notebook Overview & Workflow

The notebook contains the experimental research phase on the **IBM Telco Customer Churn dataset** (7,043 customers, 21 columns) to predict which customers are likely to churn (baseline churn rate = **26.5%**).

```
[Load & Clean] ➔ [EDA Plots] ➔ [Feature Engineering] ➔ [10-Model Benchmark] ➔ [SMOTE Oversampling] ➔ [Tuning & Metrics] ➔ [Insights]
```

---

## 1. Preprocessing & Data Cleaning

### A. Imputing TotalCharges
- **What it is**: Converting blank values in `TotalCharges` to `NaN` and filling them with the dataset's median value ($1,397.47).
- **Why use it**: Blank spaces correspond to customers with `tenure = 0` (who haven't been billed yet). Machine learning models cannot process missing or NaN values.
- **What if we deleted them?**: We would lose customer records.
- **What if we filled them with 0?**: Filling them with 0 or the median keeps the data statistically consistent.

---

## 2. Feature Engineering

### A. Feature Scaling (`StandardScaler`)
- **What it is**: Centering numerical values (like `tenure` and `TotalCharges`) to a mean of 0 and standard deviation of 1.
- **Why use it**: Models calculate importances using weights or coefficients. If one feature has values up to 8,000 (`TotalCharges`) and another up to 72 (`tenure`), the model will assume `TotalCharges` is mathematically more important. Scaling normalizes the features.
- **Analogy**: It is like rating an apple and a watermelon on a scale of 1-10 based on how they compare to others of their own kind, rather than comparing their raw weights.

### B. One-Hot Encoding
- **What it is**: Converting text categories with multiple options (like contract type: Month-to-month, One year, Two year) into separate binary columns (`0` or `1`).
- **Why use it**: Models cannot compute mathematical equations on words.
- **What if we labeled them 1, 2, 3?**: The model would assume that contract type 3 (Two year) is "three times greater" than contract type 1 (Month-to-month), which is mathematically incorrect.

---

## 3. Class Imbalance Handling (SMOTE)

- **What it is**: **Synthetic Minority Over-sampling Technique**. Since only 26.5% of customers churned, the dataset is imbalanced. SMOTE mathematically creates synthetic, realistic profiles of churned customers to balance the dataset 50/50 during training.
- **Why use it**: Without SMOTE, a model will focus on the 73.5% majority class and miss the minority churn class. By balancing the training set, we boost model **Recall by +23.5%**.
- **What if we didn't use SMOTE?**: The model would predict "No Churn" for almost everyone. It would show high accuracy on paper but fail to detect actual customers who leave.
- **Why prioritize Recall over Precision?**: For churn, missing a churner (False Negative) costs the business subscription revenue. A false alarm (False Positive) only costs a discount or a phone call. Therefore, high recall is preferred.

---

## 4. Baseline Model Comparison (10 Algorithms)

To find the strongest learning algorithm, 10 classifiers were benchmarked under 5-Fold Stratified Cross-Validation:

| Model | Accuracy | Precision | Recall | F1 Score | ROC AUC |
|---|---|---|---|---|---|
| **Voting Classifier** | 0.803 | 0.663 | 0.527 | 0.587 | **0.844** |
| AdaBoost | 0.805 | 0.669 | 0.524 | 0.588 | **0.843** |
| Logistic Regression | 0.739 | 0.505 | 0.783 | 0.614 | **0.842** |
| **Gradient Boosting** | 0.797 | 0.650 | 0.746 | 0.628 | **0.840** |
| Random Forest | 0.784 | 0.621 | 0.473 | 0.537 | 0.826 |
| Support Vector Machine (SVM) | 0.792 | 0.641 | 0.485 | 0.552 | 0.821 |
| K-Nearest Neighbors (KNN) | 0.763 | 0.562 | 0.451 | 0.501 | 0.789 |
| Decision Tree | 0.728 | 0.489 | 0.502 | 0.495 | 0.658 |
| Naive Bayes | 0.691 | 0.442 | 0.821 | 0.575 | 0.815 |

### Why Gradient Boosting?
- **Why this model?** Gradient Boosting builds sequential trees where each new tree learns from the errors of the prior trees. It achieved the best balance of F1-Score (0.628) and ROC AUC (0.84) on our dataset.
- **What if we used deep learning?**: Deep learning requires large amounts of data, takes longer to train, and consumes more RAM. Tree-based ensembles are superior for tabular datasets of this scale.
