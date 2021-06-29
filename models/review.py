#!/usr/bin/python3
"""
reviews module
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    defines the Review class

    Attributes:
    Place_id(str)
    User_id(str)
    text(str)
    """
    place_id = ""
    user_id = ""
    text = ""
