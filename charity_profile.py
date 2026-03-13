# charity_profile.py
# Defines the default charity context values used to estimate impact.

def default_charity_context():
    return {
        "charity_name": "",
        "data_sensitivity": 0,
        "operational_dependency": 0,
        "financial_exposure": 0,
        "reputational_risk": 0,
    }
