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
        fmt = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs is not None:
            for k, v in kwargs.items():
                if k == "updated_at" or k == "created_at":
                    self.__dict__[k] = datetime.strptime(v, fmt)
                else:
                    self.__dict__[k] = v
        models.storage.new(self)

    def save(self):
        """update updated_at attribute with current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """returns BaseModel dictionary instance"""
        Bdict = self.__dict__.copy()
        Bdict["created_at"] = self.created_at.isoformat()
        Bdict["updated_at"] = self.updated_at.isoformat()
        Bdict["__class__"] = self.__class__.__name__
        return Bdict

    def __str__(self):
        """returns a string representation of an instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
