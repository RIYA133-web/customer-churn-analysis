# Customer Churn Analysis & Prediction Engine

A complete churn analytics pipeline — from raw customer data to a live prediction dashboard with automated retention recommendations.

**Live Demo:** https://customer-churn-analysis-lwbx.onrender.com

---

## What This Project Does

Most churn projects stop at "here's a model that predicts churn." This one goes further:

1. **Analyzes** churn patterns across time, customer segments, and feature usage
2. **Predicts** churn probability for any customer using a trained Random Forest model
3. **Recommends** a specific retention action for each at-risk customer (not just a risk score)
4. **Serves** all of this through a live web app — anyone can input customer data and get an instant prediction + action plan

---

## Project Structure

```
customer-churn-analysis/
├── app.py                          # Flask app entrypoint
├── requirements.txt
├── src/
│   ├── model.py                    # Loads trained model, encodes input features
│   └── playbook.py                 # Risk segmentation + retention action rules
├── models/
│   ├── churn_model_v1.pkl          # Trained Random Forest classifier
│   └── feature_importance.json
├── data/
│   ├── raw/customers.csv           # Source dataset (Telco Customer Churn)
│   └── processed/                  # Feature-engineered + playbook output
├── notebooks/
│   ├── 01_eda.ipynb                # Exploratory data analysis
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb     # Model training + evaluation
│   ├── 04_root_cause_analysis.ipynb # SHAP-based churn driver analysis
│   └── 05_churn_playbook.ipynb     # Risk segmentation + action rules
├── reports/                        # Generated charts/visualizations
├── sql/                            # SQL queries used in analysis
├── templates/                      # Flask HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── predict.html
│   └── playbook.html
└── static/css/style.css
```

---

## Tech Stack

- **Python** — pandas, scikit-learn, SHAP
- **Flask** — web app / API layer
- **SQL** — data extraction queries
- **Model** — Random Forest Classifier (200 estimators, balanced class weights)

---

## How It Works

### 1. Data Pipeline (notebooks 01–02)
Raw Telco customer data → cleaned, encoded, and engineered into 35 features including tenure ratios, service counts, and value flags.

### 2. Model Training (notebook 03)
Random Forest trained on the engineered features, saved as `models/churn_model_v1.pkl`.

### 3. Root Cause Analysis (notebook 04)
SHAP values used to identify which features actually drive churn — not just correlation, but causal contribution per prediction.

### 4. Churn Playbook (notebook 05)
Each customer is assigned a `risk_segment` (Low / Medium / High) and a `recommended_action` based on rules combining churn probability, customer value, tenure, and service usage:

| Condition | Action |
|---|---|
| High value + High risk | Assign dedicated support agent |
| New customer + High risk | Send onboarding assistance email |
| Low service adoption + High risk | Offer service bundle discount |
| Medium risk | Send re-engagement email |
| High risk (no other rule matched) | Offer retention discount |
| Low risk | No action needed |

### 5. Web App (Flask)
- `/` — Dashboard with churn rate, risk segment breakdown, and action distribution
- `/predict` — Live form: input any customer's details, get instant churn probability + recommended action
- `/playbook` — Reference table of all retention rules

---

## Running Locally

```bash
git clone https://github.com/RIYA133-web/customer-churn-analysis.git
cd customer-churn-analysis
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`

---

## Dataset

[Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) — 7,043 customers, 21 original features, 26.5% churn rate.
