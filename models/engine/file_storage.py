#!/usr/bin/python3
"""
File storage module
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """serializes instances to a JSON file and deserializes
    JSON file to instances"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """ sets in __objects the obj with key
        <obj class name>.id"""
        FileStorage.__objects["{}.{}".format(obj.__class__.__name__,
                                             obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file"""
        dict_o = FileStorage.__objects
        obj_dict = {obj: dict_o[obj].to_dict() for obj in dict_o.keys()}

        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path) as f:
                obj_dict = json.load(f)
                for item in obj_dict.values():
                    class_name = item["__class__"]
                    del item["__class__"]
                    self.new(eval(class_name)(**item))
        except FileNotFoundError:
            return
