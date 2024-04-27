#!/usr/bin/python3
"""Module that tests the City model."""
import os
import unittest
from datetime import datetime
import json
from models import storage
from models.state import State
from models.city import City
from models.base_model import BaseModel, Base


STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class Test_City_File_Storage(unittest.TestCase):
    """Test class for the city model."""
    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    @classmethod
    def setUpClass(cls):
        """Set up any necessary resources for the test cases."""
        try:
            os.rename('file.json', 'tmp.json')
            cls.name = 'City'
            cls.value = City
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
                city is created properly."""
        city_instance = self.value()
        self.assertEqual(type(city_instance), self.value)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs(self):
        """
        Test case to check if an instance of city\
                can be created with keyword arguments.
        """
        city_instance = self.value()
        copy = city_instance.to_dict()
        new = City(**copy)
        self.assertFalse(new is city_instance)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_int(self):
        """
        Test case to check if TypeError is raised when\
                creating city instance with integer keys.
        """
        city_instance = self.value()
        copy = city_instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = City(**copy)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_save(self):
        """Test case to check if the 'save' method saves \
                the city instance properly."""
        city_instance = self.value()
        city_instance.save()
        key = self.name + "." + city_instance.id
        with open('file.json', 'r') as f:
            objs = json.load(f)
            self.assertEqual(objs[key], city_instance.to_dict())

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_str(self):
        """Test case to check if the 'str' method returns\
                the expected string representation."""
        city_instance = self.value()
        self.assertEqual(str(city_instance),
                         '[{}] ({}) {}'.format(self.name,
                                               city_instance.id,
                                               city_instance.__dict__))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_todict(self):
        """Test case to check if the 'to_dict' method
                returns a dictionary representation of
                the city instance.
        """
        city_instance = self.value()
        n = city_instance.to_dict()
        self.assertEqual(city_instance.to_dict(), n)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_none(self):
        """Test case to check if TypeError is raised\
                when creating city instance with None keys."""
        none_dict = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**none_dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_id(self):
        """Test case to check the data type of the 'id' attribute."""
        city_instance = self.value()
        self.assertEqual(type(city_instance.id), str)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_created_at(self):
        """Test case to check the data\
                type of the 'created_at' attribute."""
        city_instance = self.value()
        self.assertEqual(type(city_instance.created_at), datetime)


class Test_City_DBStorage(unittest.TestCase):
    """Test class for the city model."""
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing FileStorage')
    @classmethod
    def setUpClass(cls):
        """
        setting up class
        """
        cls.storage = storage
        cls.storage.reload()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)

        cls.storage.new(cls.state)
        cls.storage.new(cls.city)
        cls.storage.save()

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing FileStorage')
    @classmethod
    def tearDownClass(cls) -> None:
        """
        tear down class set up
        """
        cls.storage.reload()
        for city in cls.storage.all('City'):
            if cls.city == city:
                cls.storage._DBStorage__session.delete(cls.city)
        for state in cls.storage.all('State'):
            if cls.state == state:
                cls.storage._DBStorage__session.delete(cls.state)
        cls.storage.save()
        cls.storage.close()

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_is_basemodel_subclass(self):
        """
        test class name
        """
        self.assertIsInstance(self.city, BaseModel)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_attr(self):
        """
        test class name
        """
        self.assertTrue(hasattr(self.city, 'name'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_attr(self):
        """
        test class id attribute
        """
        self.assertTrue(hasattr(self.city, 'id'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_attr(self):
        """
        test class updated_at attribute
        """
        self.assertTrue(hasattr(self.city, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.city, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_value_none(self):
        """
        test class name
        """
        self.assertNotEqual(self.city.name, None)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_value(self):
        """
        test class id
        """
        self.assertIsNotNone(self.city.id)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_value(self):
        """
        test class updated_at
        """
        self.assertIsNotNone(self.city.updated_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_value(self):
        """
        test class created_at
        """
        self.assertIsNotNone(self.city.created_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_with_value(self):
        """
        test class created_at
        """
        self.city.name = "Nairobi"
        self.assertTrue(self.city.name)
        self.assertEqual(self.city.name, "Nairobi")

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict(self):
        """
        test class created_at
        """
        self.assertEqual(type(self.city.to_dict()), dict)
        self.assertFalse('_sa_instance_state' in self.city.to_dict())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict_values(self):
        """
        test class created_at
        """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        class_name = self.city.to_dict().get('__class__')
        city_id = self.city.to_dict().get('id')
        city_name = self.city.to_dict().get('name')
        created_at = self.city.to_dict().get('created_at')
        updated_at = self.city.to_dict().get('updated_at')
        places = self.city.to_dict().get('places')

        self.assertEqual(class_name, 'City')
        self.assertEqual(type(city_id), str)
        self.assertEqual(type(city_name), str)
        self.assertEqual(created_at, self.city.created_at.strftime(t_format))
        self.assertEqual(updated_at, self.city.updated_at.strftime(t_format))
        self.assertEqual(places, None)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_sa_subclass(self):
        """
        test that city is subclass of declarative base
        """
        self.assertTrue(isinstance(self.city, Base))
        self.assertTrue('_sa_instance_state' in self.city.__dict__)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_str(self):
        """test that the str method has the correct output"""
        am_dict = self.city.__dict__
        am_dict.pop('_sa_instance_state')
        string = "[City] ({}) {}".format(self.city.id, am_dict)
        self.assertEqual(string, str(self.city))


if __name__ == '__main__':
    unittest.main()
