# charity_profile.py
# defines the default charity context values used to estimate impact

def default_charity_context():
    # kept these factors simple so impact reflects what actually affects small charities most:
    # sensitive data, reliance on systems, money, and reputation

    return {
        "charity_name": "",
        "data_sensitivity": 0,   # defaults are set to 0 so the user must actively choose values             
        "operational_dependency": 0, # it helps avoide inflated risk scores from assumptions
        "financial_exposure": 0,
        "reputational_risk": 0,
    }