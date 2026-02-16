# Questionnaire Import and Validation
# This module is responsible for loading the questionnaire data from a CSV file using Pandas. 
# Since your tool is data-driven, this file enables you to modify or expand the questionnaire without changing your codebase. 
# The script will include functions that (1) read the questionnaire, (2) validate required columns, and (3) prepare the data in a structured format for downstream processing. 
# In the context of your project, the data loader plays a crucial role in ensuring that the scoring engine works consistently regardless of the questionnaire format allowing your tool to remain flexible and scalable.

# data_loader.py
# Lightweight storage helpers (optional)
# Use JSON for simplicity (no pandas needed yet)

import json



def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    
def context_templates():
    return {
        "Micro charity (0–9 people)": {"data_sensitivity": 2, "operational_dependency": 2, "financial_exposure": 1, "reputational_risk": 2},
        "Small charity (10–49 people)": {"data_sensitivity": 3, "operational_dependency": 3, "financial_exposure": 2, "reputational_risk": 3},
        "Medium charity (50–249 people)": {"data_sensitivity": 3, "operational_dependency": 4, "financial_exposure": 3, "reputational_risk": 4},
    }




