import os
import json
import pandas as pd
from flask import Flask, render_template, request

from src.model import predict_churn
from src.playbook import assign_risk, churn_playbook, ACTION_DESCRIPTIONS

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')


def load_dashboard_stats():
    """Load summary stats from processed churn_playbook.csv if it exists."""
    stats = {
        'total_customers': 7043,
        'churn_rate': 26.5,
        'high_risk': 0,
        'medium_risk': 0,
        'low_risk': 0,
        'action_counts': {},
        'has_data': False
    }
    csv_path = os.path.join(PROCESSED_DIR, 'churn_playbook.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        stats['total_customers'] = len(df)
        stats['churn_rate'] = round(df['Churn'].mean() * 100, 1)
        counts = df['risk_segment'].value_counts().to_dict()
        stats['high_risk'] = counts.get('High Risk', 0)
        stats['medium_risk'] = counts.get('Medium Risk', 0)
        stats['low_risk'] = counts.get('Low Risk', 0)
        stats['action_counts'] = df['recommended_action'].value_counts().to_dict()
        stats['has_data'] = True
    return stats


@app.route('/')
def dashboard():
    stats = load_dashboard_stats()
    return render_template('dashboard.html', stats=stats)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    result = None
    if request.method == 'POST':
        form = request.form
        prob, total_services = predict_churn(form)
        risk_segment = assign_risk(prob)
        action = churn_playbook(
            prob=prob,
            is_high_value=1 if float(form.get('monthly_charges', 0)) >= 70 else 0,
            is_new_customer=1 if float(form.get('tenure', 0)) <= 6 else 0,
            total_services=total_services
        )
        result = {
            'probability': round(prob * 100, 1),
            'risk_segment': risk_segment,
            'action': action,
            'action_description': ACTION_DESCRIPTIONS.get(action, '')
        }
    return render_template('predict.html', result=result)


@app.route('/playbook')
def playbook():
    descriptions = ACTION_DESCRIPTIONS
    stats = load_dashboard_stats()
    return render_template('playbook.html', descriptions=descriptions, stats=stats)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
