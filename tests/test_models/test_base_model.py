#!/usr/bin/python3
"""Unittest for basemodel module"""
import models
import os
import unittest
from time import sleep
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Testing instantiation attributes"""

    def test_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_str_public(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        inst1 = BaseModel()
        inst2 = BaseModel()
        self.assertNotEqual(inst1.id, inst2.id)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        bm_str = bm.__str__()
        self.assertIn("[BaseModel] (123456)", bm_str)
        self.assertIn("'id': '123456'", bm_str)
        self.assertIn("'created_at': " + dt_repr, bm_str)
        self.assertIn("'updated_at': " + dt_repr, bm_str)

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Testing BaseModel's save method"""
    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def test_single_save(self):
        bm = BaseModel()
        sleep(0.05)
        first = bm.updated_at
        bm.save()
        self.assertLess(first, bm.updated_at)

    def test_two_saves(self):
        bm = BaseModel()
        sleep(0.05)
        first = bm.updated_at
        bm.save()
        second = bm.updated_at
        self.assertLess(first, second)
        sleep(0.05)
        bm.save()
        self.assertLess(second, bm.updated_at)

    def test_save_updates_file(self):
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """testing the to_dict method of BaseModel"""

    def test_to_dict_type(self):
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_correct_keys(self):
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_with_added_attributes(self):
        bm = BaseModel()
        bm.name = "Holberton"
        self.assertIn("name", bm.to_dict())

    def test_contrast_to_dict_dunder_dict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_output(self):
        dt = datetime.today()
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

if __name__ == "__main__":
    unittest.main()
