#!/usr/bin/env python3
"""
Crossmint challenge - phase 1 code
"""

import json
import requests
from variables import BASE_API, CANDIDATE_ID

# Common variables
DATA = {"candidateId": CANDIDATE_ID}
POLYANETS = "polyanets"
SOLOONS = "soloons"
COMETH = "comeths"
GOAL = f"map/{CANDIDATE_ID}/goal"

# Getting the target shape
GOAL_RSP = requests.get(BASE_API + GOAL, data=DATA)
GOAL_SHAPE = json.loads(GOAL_RSP.text)["goal"]

if __name__ == "__main__":
    # Implementing the shape
    for i, row in enumerate(GOAL_SHAPE):
        for j, col in enumerate(row):
            if col == "POLYANET":
                # Update coordinates
                DATA.update({"row": i, "column": j})

                # Draw polyanet
                requests.post(BASE_API + POLYANETS, data=DATA)
