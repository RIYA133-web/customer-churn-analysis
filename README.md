
# 🎯 Customer Churn Analysis — Deep Dive + Action Playbook

> Predicting **why** customers leave, not just **who** will leave — with a business playbook that turns predictions into real actions.

---

## 📌 Problem Statement

A company is losing customers but doesn't know why. This project goes beyond building a churn prediction model — it performs a full **root cause analysis** and delivers a **Churn Playbook** with automated action recommendations for every at-risk customer.

---

## 🚀 Live Demo (Flask App)

```bash
python app.py
```
Open `http://localhost:5000` in your browser.

Features:
- Upload your own company CSV
- View churn dashboard with charts
- Predict churn risk for a single customer

---

## 📊 Results

| Metric | Score |
|--------|-------|
| Model | Random Forest |
| ROC-AUC (Mean) | 0.844 |
| ROC-AUC (Std Dev) | 0.012 |
| Cross Validation | 5-Fold |
| Dataset Size | 7,043 customers |

---

## 🔍 Key Findings

- **Month-to-month** contract customers churn at 3x the rate of yearly contracts
- **New customers** (tenure < 12 months) are the highest churn risk group
- **High monthly charges + low tenure** is the strongest churn signal
- Customers with **no online security or tech support** are significantly more likely to churn
- **Fiber optic** internet users churn more than DSL users despite paying more

---

## 🗂️ Project Structure

```
customer-churn-analysis/
│
├── app.py                          # Flask web application
│
├── notebooks/
│   ├── 01_eda.ipynb                # Exploratory data analysis
│   ├── 02_feature_engineering.ipynb # Feature creation + encoding
│   ├── 03_model_training.ipynb     # Random Forest training + evaluation
│   ├── 04_root_cause_analysis.ipynb # SHAP root cause analysis
│   └── 05_churn_playbook.ipynb     # Business action rule engine
│
├── src/
│   ├── data_loader.py              # Load + clean raw data
│   ├── feature_engineering.py      # Build churn signals
│   ├── model.py                    # Predict + explain
│   └── playbook.py                 # Action rule engine
│
├── data/
│   ├── raw/customers.csv           # Raw Kaggle dataset
│   └── processed/                  # Cleaned + engineered features
│
├── models/
│   ├── churn_model_v1.pkl          # Trained Random Forest model
│   └── feature_importance.json     # Top features driving churn
│
├── reports/                        # Generated charts + visuals
├── sql/                            # SQL queries for production use
├── templates/                      # Flask HTML templates
├── static/                         # CSS + JS assets
├── config.yaml                     # Column mapping for custom datasets
└── requirements.txt
```

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/customer-churn-analysis.git
cd customer-churn-analysis
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the dataset
- Go to: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- Download `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- Place it in `data/raw/customers.csv`

### 5. Run notebooks in order
```
notebooks/01_eda.ipynb
notebooks/02_feature_engineering.ipynb
notebooks/03_model_training.ipynb
notebooks/04_root_cause_analysis.ipynb
notebooks/05_churn_playbook.ipynb
```

### 6. Launch the Flask app
```bash
python app.py
```

---

## 🧠 Churn Playbook Rules

| Condition | Action |
|-----------|--------|
| High value customer + churn prob ≥ 0.7 | Assign dedicated support agent |
| New customer + churn prob ≥ 0.6 | Send onboarding assistance email |
| Low services + churn prob ≥ 0.6 | Offer service bundle discount |
| Churn prob between 0.4 – 0.7 | Send re-engagement email |
| Churn prob ≥ 0.7 (none of above) | Offer retention discount |
| Churn prob < 0.4 | No action needed |

---

## 🔧 Using Your Own Company Data

This project supports any company's customer data via `config.yaml`:

```yaml
column_mapping:
  churn          : cancelled        # your churn column name
  monthly_charges: monthly_revenue  # your revenue column
  tenure         : tenure_months    # months as customer
  join_date      : signup_date      # when they joined
  last_active    : last_login_date  # last activity date

thresholds:
  high_risk    : 0.7
  medium_risk  : 0.4
  new_customer : 12     # months
```

**Steps to adapt:**
1. Export your customer data as CSV → place in `data/raw/customers.csv`
2. Update column names in `config.yaml`
3. Adjust feature logic in `02_feature_engineering.ipynb`
4. Run all notebooks — model + playbook auto-adapt to your data

---

## 🗃️ SQL Queries (Production Use)

In a real company, data lives in databases. The `sql/` folder contains queries for:

```
sql/churn_monthly_trend.sql     # Monthly churn rate over time
sql/new_vs_old_customers.sql    # Churn by customer type
sql/feature_usage.sql           # Churn by service usage
sql/high_value_users.sql        # High value customers at risk
```

---

## 📈 Charts Generated

| Chart | Description |
|-------|-------------|
| `churn_distribution.png` | Overall churn vs retained |
| `churn_by_contract.png` | Churn rate by contract type |
| `churn_by_tenure.png` | Churn trend over customer lifetime |
| `charges_distribution.png` | Monthly charges for churned vs retained |
| `correlation_heatmap.png` | Feature correlations |
| `confusion_matrix.png` | Model prediction accuracy |
| `roc_curve.png` | ROC-AUC curve |
| `feature_importance.png` | Top features driving churn |
| `shap_importance.png` | SHAP feature importance |
| `shap_dot_plot.png` | SHAP impact direction |
| `playbook_actions.png` | Distribution of recommended actions |

---

## 🛠️ Tools & Technologies

| Category | Tools |
|----------|-------|
| Language | Python 3.10 |
| Data | Pandas, NumPy |
| Modeling | Scikit-learn (Random Forest) |
| Explainability | SHAP |
| Visualization | Matplotlib, Seaborn |
| Web App | Flask |
| Database | SQL (MySQL / PostgreSQL compatible) |
| Environment | Jupyter Notebook, VS Code |

---

## 📄 Dataset

**Telco Customer Churn** — IBM Sample Dataset via Kaggle  
Link: https://www.kaggle.com/datasets/blastchar/telco-customer-churn  
Size: 7,043 customers, 21 features

---

## 💼 Resume Description

```
Customer Churn Analysis & Prediction | Python, Scikit-learn, SHAP, Flask
- Built end-to-end churn prediction pipeline with Random Forest (ROC-AUC: 0.844)
- Performed root cause analysis using SHAP to identify top churn drivers
- Designed Churn Playbook with 6 automated business action rules
- Built Flask web app for uploading company data and viewing churn dashboard
- Wrote production-ready SQL queries for real-world database integration
```

---

## 📃 License

MIT License — free to use and adapt for your own company data.
