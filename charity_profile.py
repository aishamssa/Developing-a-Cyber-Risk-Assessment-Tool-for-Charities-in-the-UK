# Data Structure for Storing Results
# This module defines a simple class that represents a charity’s responses, intermediate scores, and final risk outcome. 
# While the system can be built without classes, storing results in a structured object improves clarity, testing, and traceability. 
# The charity profile object can later be used to generate recommendations, export results, or store historical assessments. 
# Including this module demonstrates that you understand how to model data in a way that aligns with real-world software-engineering practice.

# charity_profile.py
# Charity context used to estimate IMPACT (NIST SP 800-30 concept: impact magnitude)


def default_charity_context():
    return {
        "charity_name": "",
        "data_sensitivity": 2,
        "operational_dependency": 2,
        "financial_exposure": 2,
        "reputational_risk": 2,
    }
