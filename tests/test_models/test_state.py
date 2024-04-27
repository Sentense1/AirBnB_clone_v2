#!/usr/bin/python3
"""Module that tests the state model."""
import os
import unittest
from datetime import datetime
import json
from models import storage
from models.state import State
from models.base_model import BaseModel, Base


STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class Test_State_File_Storage(unittest.TestCase):
    """Test class for the state model."""
    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    @classmethod
    def setUpClass(cls):
        """Set up any necessary resources for the test cases."""
        try:
            os.rename('file.json', 'tmp.json')
            cls.name = 'State'
            cls.value = State
        except Exception:
            pass

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    @classmethod
    def tearDownClass(cls):
        """Clean up any resources created during the test cases."""
        try:
            os.rename('tmp.json', 'file.json')
            del cls.name
            del cls.value
        except Exception:
            pass

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_default(self):
        """Test case to check if an instance of \
                state is created properly."""
        state_instance = self.value()
        self.assertEqual(type(state_instance), self.value)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs(self):
        """
        Test case to check if an instance of state\
                can be created with keyword arguments.
        """
        state_instance = self.value()
        copy = state_instance.to_dict()
        new = State(**copy)
        self.assertFalse(new is state_instance)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_int(self):
        """
        Test case to check if TypeError is raised when\
                creating state instance with integer keys.
        """
        state_instance = self.value()
        copy = state_instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = State(**copy)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_save(self):
        """Test case to check if the 'save' method saves \
                the state instance properly."""
        state_instance = self.value()
        state_instance.save()
        key = self.name + "." + state_instance.id
        with open('file.json', 'r') as f:
            objs = json.load(f)
            self.assertEqual(objs[key], state_instance.to_dict())

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_str(self):
        """Test case to check if the 'str' method returns\
                the expected string representation."""
        state_instance = self.value()
        self.assertEqual(str(state_instance),
                         '[{}] ({}) {}'.format(self.name,
                                               state_instance.id,
                                               state_instance.__dict__))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_todict(self):
        """Test case to check if the 'to_dict' method
                returns a dictionary representation of
                the state instance.
        """
        state_instance = self.value()
        n = state_instance.to_dict()
        self.assertEqual(state_instance.to_dict(), n)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_none(self):
        """Test case to check if TypeError is raised\
                when creating state instance with None keys."""
        none_dict = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**none_dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_id(self):
        """Test case to check the data type of the 'id' attribute."""
        state_instance = self.value()
        self.assertEqual(type(state_instance.id), str)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_created_at(self):
        """Test case to check the data\
                type of the 'created_at' attribute."""
        state_instance = self.value()
        self.assertEqual(type(state_instance.created_at), datetime)


class Test_state_DBStorage(unittest.TestCase):
    """Test class for the state model."""
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing FileStorage')
    @classmethod
    def setUpClass(cls):
        """
        setting up class
        """
        cls.storage = storage
        cls.storage.reload()

        cls.state = State(name="Nairobi")

        cls.storage.new(cls.state)
        cls.storage.save()

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing FileStorage')
    @classmethod
    def tearDownClass(cls) -> None:
        """
        tear down class set up
        """
        cls.storage.close()

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_is_basemodel_subclass(self):
        """
        test class name
        """
        self.assertIsInstance(self.state, BaseModel)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_attr(self):
        """
        test class name
        """
        self.assertTrue(hasattr(self.state, 'name'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_attr(self):
        """
        test class id attribute
        """
        self.assertTrue(hasattr(self.state, 'id'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_attr(self):
        """
        test class updated_at attribute
        """
        self.assertTrue(hasattr(self.state, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.state, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_value_none(self):
        """
        test class name
        """
        self.assertNotEqual(self.state.name, None)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_value(self):
        """
        test class id
        """
        self.assertIsNotNone(self.state.id)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_value(self):
        """
        test class updated_at
        """
        self.assertIsNotNone(self.state.updated_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_value(self):
        """
        test class created_at
        """
        self.assertIsNotNone(self.state.created_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_with_value(self):
        """
        test class created_at
        """
        self.assertTrue(self.state.name)
        self.assertEqual(self.state.name, "Nairobi")

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict(self):
        """
        test class created_at
        """
        self.assertEqual(type(self.state.to_dict()), dict)
        self.assertFalse('_sa_instance_state' in self.state.to_dict())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict_values(self):
        """
        test class created_at
        """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        class_name = self.state.to_dict().get('__class__')
        state_id = self.state.to_dict().get('id')
        state_name = self.state.to_dict().get('name')
        created_at = self.state.to_dict().get('created_at')
        updated_at = self.state.to_dict().get('updated_at')
        cities = self.state.to_dict().get('cities')

        self.assertEqual(class_name, 'State')
        self.assertEqual(type(state_id), str)
        self.assertEqual(type(state_name), str)
        self.assertEqual(created_at, self.state.created_at.strftime(t_format))
        self.assertEqual(updated_at, self.state.updated_at.strftime(t_format))
        self.assertEqual(cities, None)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_Base_subclass(self):
        """
        test that state is subclass of declarative base
        """
        self.assertIsInstance(self.state, Base)
        self.assertTrue('_sa_instance_state' in self.state.__dict__)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_str(self):
        """test that the str method has the correct output"""
        am_dict = self.state.__dict__
        am_dict.pop('_sa_instance_state')
        string = "[State] ({}) {}".format(self.state.id, am_dict)
        self.assertEqual(string, str(self.state))


if __name__ == '__main__':
    unittest.main()
