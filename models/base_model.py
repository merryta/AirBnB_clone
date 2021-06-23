#!/usr/bin/python3
"""BaseModel module"""
from uuid import uuid4
from datetime import datetime
import models

class BaseModel:
    """class BaseModel: defines common attributes/methods for other
    classes"""

    def __init__(self, *args, **kwargs):
        """initializes the BaseModel attributes"""

        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
