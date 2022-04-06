#!/usr/bin/env python3
"""
Crossmint challenge - phase 2 code
"""

import json
import requests
from variables import BASE_API, CANDIDATE_ID

# pylint: disable=too-few-public-methods
# pylint: disable=redefined-outer-name

# Common variables
POLYANETS = "polyanets"
SOLOONS = "soloons"
COMETH = "comeths"
GOAL = f"map/{CANDIDATE_ID}/goal"

# Getting the target shape
GOAL_RSP = requests.get(BASE_API + GOAL, data={"candidateId": CANDIDATE_ID})
GOAL_SHAPE = json.loads(GOAL_RSP.text)["goal"]

class Shape():
    """
    Base class for all astral objects
    """
    def __init__(self, row=None, column=None):
        """
        Initialize class attributes
        :param row:    int, "y" coordinate for the crossmint logo
        :param column: int, "x" coordinate for the crossmint logo
        """
        self.endpoint = BASE_API
        self.data = {"candidateId": CANDIDATE_ID, "row": row, "column": column}


class Polyanets(Shape):
    """
    Class to inherit from `Shape` and to store polyanet instances
    """
    def __init__(self, **kwargs):
        """
        Define polyanets attributes
        :param kwargs:    int, optional keyword arguments as specified for
                          the parent class: row, column
        """
        super().__init__(**kwargs)
        self.endpoint += POLYANETS


class Cometh(Shape):
    """
    Class to inherit from `Shape` and to store cometh instances
    """
    def __init__(self, variant="", **kwargs):
        """
        Define cometh attributes
        :param variant:   str, cometh variant including its direction as
                          a prefix, e.g.: "UP_COMETH"
        :param kwargs:    int, optional keyword arguments as specified for
                          the parent class: row, column
        """
        super().__init__(**kwargs)
        self.endpoint += COMETH

        # Carve out the direction from the variant and make it lowercase
        self.data["direction"] = variant.split("_")[0].lower()


class Soloons(Shape):
    """
    Class to inherit from `Shape` and to store soloon instances
    """
    def __init__(self, variant, **kwargs):
        """
        Define soloon attributes
        :param variant:   str, soloon variant including its color as a prefix
                          e.g.: "PURPLE_SOLOON"
        :param kwargs:    int, optional keyword arguments as specified for
                          the parent class: row, column
        """
        super().__init__(**kwargs)
        self.endpoint += SOLOONS

        # Carve out the color from the variant and make it lowercase
        self.data["color"] = variant.split("_")[0].lower()


if __name__ == "__main__":
    # Implementing the shape
    for i, row in enumerate(GOAL_SHAPE):
        for j, shape in enumerate(row):
            # Reset astral object
            astral_object = None

            # Build astral objects (supplying its name and coordinates)
            if shape == "POLYANET":
                astral_object = Polyanets(row=i, column=j)
            elif "COMETH" in shape:
                astral_object = Cometh(shape, row=i, column=j)
            elif "SOLOON" in shape:
                astral_object = Soloons(shape, row=i, column=j)

            # If we have an astral object (e.g. `shape` wasn't "SPACE") make request
            if astral_object:
                requests.post(astral_object.endpoint, data=astral_object.data)
            