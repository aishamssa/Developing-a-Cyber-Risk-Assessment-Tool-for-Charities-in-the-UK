# data_loader.py
# helper functions for saving and loading assessment data.
# uses JSON for lightweight storage and exporting results

import json


def save_json(filepath, data):
    # used json here so results are easy to read, share, and reuse outside the app
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    




