#!/usr/bin/python3
"""Module that tests the Amenity model."""
import os
import unittest
from datetime import datetime
import json
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models import storage


STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class Test_Amenity_File_Storage(unittest.TestCase):
    """Test class for the Amenity model."""
    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    @classmethod
    def setUpClass(cls):
        """Set up any necessary resources for the test cases."""
        try:
            os.rename('file.json', 'tmp.json')
            cls.name = 'Amenity'
            cls.value = Amenity
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
                Amenity is created properly."""
        amenity_instance = self.value()
        self.assertEqual(type(amenity_instance), self.value)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs(self):
        """
        Test case to check if an instance of Amenity\
                can be created with keyword arguments.
        """
        amenity_instance = self.value()
        copy = amenity_instance.to_dict()
        new = Amenity(**copy)
        self.assertFalse(new is amenity_instance)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_int(self):
        """
        Test case to check if TypeError is raised when\
                creating Amenity instance with integer keys.
        """
        amenity_instance = self.value()
        copy = amenity_instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = Amenity(**copy)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_save(self):
        """Test case to check if the 'save' method saves \
                the Amenity instance properly."""
        amenity_instance = self.value()
        amenity_instance.save()
        key = self.name + "." + amenity_instance.id
        with open('file.json', 'r') as f:
            objs = json.load(f)
            self.assertEqual(objs[key], amenity_instance.to_dict())

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_str(self):
        """Test case to check if the 'str' method returns\
                the expected string representation."""
        amenity_instance = self.value()
        self.assertEqual(str(amenity_instance),
                         '[{}] ({}) {}'.format(self.name,
                                               amenity_instance.id,
                                               amenity_instance.__dict__))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_todict(self):
        """Test case to check if the 'to_dict' method
                returns a dictionary representation of
                the Amenity instance.
        """
        amenity_instance = self.value()
        n = amenity_instance.to_dict()
        self.assertEqual(amenity_instance.to_dict(), n)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_none(self):
        """Test case to check if TypeError is raised\
                when creating Amenity instance with None keys."""
        none_dict = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**none_dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_id(self):
        """Test case to check the data type of the 'id' attribute."""
        amenity_instance = self.value()
        self.assertEqual(type(amenity_instance.id), str)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_created_at(self):
        """Test case to check the data\
                type of the 'created_at' attribute."""
        amenity_instance = self.value()
        self.assertEqual(type(amenity_instance.created_at), datetime)


class Test_Amenity_DBStorage(unittest.TestCase):
    """Test class for the Amenity model."""
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
        cls.user = User(email="johnson@example.com", password="johnson")
        cls.place = Place(name="Cozy Apartment", city_id=cls.city.id,
                          user_id=cls.user.id)

        cls.amenity = Amenity(name="WIFI")
        cls.place.amenities.append(cls.amenity)
        cls.storage.new(cls.state)
        cls.storage.new(cls.city)
        cls.storage.new(cls.user)
        cls.storage.new(cls.place)
        cls.storage.new(cls.amenity)
        cls.storage.save()

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing FileStorage')
    @classmethod
    def tearDownClass(cls) -> None:
        """
        tear down class set up
        """
        cls.storage.reload()
        # for am in cls.place.amenities:
        #     cls.storage._DBStorage__session.remove(am)
        for user in cls.storage.all('User'):
            if cls.user == user:
                cls.storage._DBStorage__session.delete(cls.user)
        for state in cls.storage.all('State'):
            if cls.state == state:
                cls.storage._DBStorage__session.delete(cls.state)
        for place in cls.storage.all('Place'):
            if cls.place == place:
                cls.storage._DBStorage__session.delete(cls.place)
        for am in cls.storage.all('Amenity'):
            if cls.amenity == am:
                cls.storage._DBStorage__session.delete(cls.amenity)
        cls.storage.save()
        cls.storage.close()

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_is_basemodel_subclass(self):
        """
        test class name
        """
        self.assertIsInstance(self.amenity, BaseModel)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_attr(self):
        """
        test class name
        """
        self.assertTrue(hasattr(self.amenity, 'name'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_attr(self):
        """
        test class id attribute
        """
        self.assertTrue(hasattr(self.amenity, 'id'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_attr(self):
        """
        test class updated_at attribute
        """
        self.assertTrue(hasattr(self.amenity, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.amenity, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_value_none(self):
        """
        test class name
        """
        self.assertNotEqual(self.amenity.name, None)
        self.assertEqual(self.amenity.name, 'WIFI')

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_value(self):
        """
        test class id
        """
        self.assertIsNotNone(self.amenity.id)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_value(self):
        """
        test class updated_at
        """
        self.assertIsNotNone(self.amenity.updated_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_value(self):
        """
        test class created_at
        """
        self.assertIsNotNone(self.amenity.created_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_with_value(self):
        """
        test class created_at
        """
        self.assertTrue(self.amenity.name)
        self.assertEqual(self.amenity.name, "WIFI")

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict(self):
        """
        test class created_at
        """
        self.assertEqual(type(self.amenity.to_dict()), dict)
        self.assertFalse('_sa_instance_state' in self.amenity.to_dict())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict_values(self):
        """
        test class created_at
        """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        class_name = self.amenity.to_dict().get('__class__')
        amenity_id = self.amenity.to_dict().get('id')
        amenity_name = self.amenity.to_dict().get('name')
        created_at = self.amenity.to_dict().get('created_at')
        updated_at = self.amenity.to_dict().get('updated_at')

        self.assertEqual(class_name, 'Amenity')
        self.assertEqual(type(amenity_id), str)
        self.assertEqual(type(amenity_name), str)
        self.assertEqual(created_at,
                         self.amenity.created_at.strftime(t_format))
        self.assertEqual(updated_at,
                         self.amenity.updated_at.strftime(t_format))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_Base_subclass(self):
        """
        test that amenity is subclass of declarative base
        """
        self.assertIsInstance(self.amenity, Base)
        self.assertTrue('_sa_instance_state' in self.amenity.__dict__)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_str(self):
        """test that the str method has the correct output"""
        am_dict = self.amenity.__dict__
        am_dict.pop('_sa_instance_state')
        string = "[Amenity] ({}) {}".format(self.amenity.id, am_dict)
        self.assertEqual(string, str(self.amenity))


if __name__ == '__main__':
    unittest.main()
