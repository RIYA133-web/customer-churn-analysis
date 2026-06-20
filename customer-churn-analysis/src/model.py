import pickle
import os
import numpy as np
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'churn_model_v1.pkl')

FEATURE_COLUMNS = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService',
    'PaperlessBilling', 'MonthlyCharges', 'TotalCharges', 'charge_per_tenure',
    'total_services', 'is_new_customer', 'is_high_value', 'no_support_services',
    'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year',
    'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check'
]

_model = None


def get_model():
    global _model
    if _model is None:
        with open(MODEL_PATH, 'rb') as f:
            _model = pickle.load(f)
    return _model


def build_feature_row(form):
    """
    Build a single-row DataFrame matching FEATURE_COLUMNS from raw form input.
    `form` is a dict with simple human-readable keys.
    """
    row = {col: 0 for col in FEATURE_COLUMNS}

    # Basic numeric / binary fields
    row['gender'] = 1 if form.get('gender') == 'Male' else 0
    row['SeniorCitizen'] = int(form.get('senior_citizen', 0))
    row['Partner'] = 1 if form.get('partner') == 'Yes' else 0
    row['Dependents'] = 1 if form.get('dependents') == 'Yes' else 0
    row['PhoneService'] = 1 if form.get('phone_service') == 'Yes' else 0
    row['PaperlessBilling'] = 1 if form.get('paperless_billing') == 'Yes' else 0

    tenure_months = float(form.get('tenure', 0))
    monthly_charges = float(form.get('monthly_charges', 0))
    total_charges = float(form.get('total_charges', monthly_charges * tenure_months))

    # Notebook 02 normalized tenure/charges (min-max). Approximation using
    # known Telco dataset ranges: tenure 0-72, monthly 18.25-118.75, total 18.8-8684.8
    row['tenure'] = tenure_months / 72.0
    row['MonthlyCharges'] = (monthly_charges - 18.25) / (118.75 - 18.25)
    row['TotalCharges'] = (total_charges - 18.8) / (8684.8 - 18.8)

    row['charge_per_tenure'] = monthly_charges / (tenure_months + 1)

    # Count services
    service_flags = [
        form.get('phone_service') == 'Yes',
        form.get('multiple_lines') == 'Yes',
        form.get('internet_service') in ('DSL', 'Fiber optic'),
        form.get('online_security') == 'Yes',
        form.get('online_backup') == 'Yes',
        form.get('device_protection') == 'Yes',
        form.get('tech_support') == 'Yes',
        form.get('streaming_tv') == 'Yes',
        form.get('streaming_movies') == 'Yes',
    ]
    total_services = sum(1 for s in service_flags if s)
    row['total_services'] = total_services
    row['no_support_services'] = 1 if (
        form.get('online_security') != 'Yes' and
        form.get('tech_support') != 'Yes' and
        form.get('device_protection') != 'Yes'
    ) else 0

    row['is_new_customer'] = 1 if tenure_months <= 6 else 0
    row['is_high_value'] = 1 if monthly_charges >= 70 else 0

    # MultipleLines
    if form.get('phone_service') != 'Yes':
        row['MultipleLines_No phone service'] = 1
    elif form.get('multiple_lines') == 'Yes':
        row['MultipleLines_Yes'] = 1

    # InternetService
    internet = form.get('internet_service', 'No')
    if internet == 'Fiber optic':
        row['InternetService_Fiber optic'] = 1
    elif internet == 'No':
        row['InternetService_No'] = 1

    def encode_addon(field_key, col_prefix):
        val = form.get(field_key, 'No')
        if internet == 'No':
            row[f'{col_prefix}_No internet service'] = 1
        elif val == 'Yes':
            row[f'{col_prefix}_Yes'] = 1

    encode_addon('online_security', 'OnlineSecurity')
    encode_addon('online_backup', 'OnlineBackup')
    encode_addon('device_protection', 'DeviceProtection')
    encode_addon('tech_support', 'TechSupport')
    encode_addon('streaming_tv', 'StreamingTV')
    encode_addon('streaming_movies', 'StreamingMovies')

    # Contract
    contract = form.get('contract', 'Month-to-month')
    if contract == 'One year':
        row['Contract_One year'] = 1
    elif contract == 'Two year':
        row['Contract_Two year'] = 1

    # PaymentMethod
    payment = form.get('payment_method', 'Electronic check')
    if payment == 'Credit card (automatic)':
        row['PaymentMethod_Credit card (automatic)'] = 1
    elif payment == 'Electronic check':
        row['PaymentMethod_Electronic check'] = 1
    elif payment == 'Mailed check':
        row['PaymentMethod_Mailed check'] = 1

    df = pd.DataFrame([row], columns=FEATURE_COLUMNS)
    return df, total_services


def predict_churn(form):
    model = get_model()
    X, total_services = build_feature_row(form)
    prob = model.predict_proba(X)[:, 1][0]
    return float(prob), total_services
