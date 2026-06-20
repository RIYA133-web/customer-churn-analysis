def assign_risk(prob):
    if prob >= 0.6:
        return 'High Risk'
    elif prob >= 0.3:
        return 'Medium Risk'
    else:
        return 'Low Risk'


def churn_playbook(prob, is_high_value, is_new_customer, total_services):
    """
    Replicates notebook 05 playbook rules.
    """
    if is_high_value == 1 and prob >= 0.7:
        return 'Assign dedicated support agent'
    elif is_new_customer == 1 and prob >= 0.6:
        return 'Send onboarding assistance email'
    elif total_services <= 2 and prob >= 0.6:
        return 'Offer service bundle discount'
    elif 0.3<= prob < 0.6:
        return 'Send re-engagement email'
    elif prob >= 0.7:
        return 'Offer retention discount'
    else:
        return 'No action needed'


ACTION_DESCRIPTIONS = {
    'Assign dedicated support agent': 'High-value customer at high risk. Route to a dedicated CSM for an immediate check-in.',
    'Send onboarding assistance email': 'New customer struggling. Send guided onboarding resources and tutorials.',
    'Offer service bundle discount': 'Low service adoption + high risk. Offer a bundle discount to increase stickiness.',
    'Send re-engagement email': 'Medium risk. Send a re-engagement campaign highlighting unused features.',
    'Offer retention discount': 'High risk, no other rule matched. Offer a retention discount to prevent churn.',
    'No action needed': 'Low risk. No action required at this time.'
}
