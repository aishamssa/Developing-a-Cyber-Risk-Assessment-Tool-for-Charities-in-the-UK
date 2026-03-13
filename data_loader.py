# data_loader.py
# Helper functions for saving and loading assessment data.
# Uses JSON for lightweight storage and exporting results.

import json


def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    




