#!/usr/bin/python3
"""Module that tests the user model."""
import os
import unittest
from datetime import datetime
import json
from models import storage
from models.user import User
from models.base_model import BaseModel, Base


STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class Test_User_File_Storage(unittest.TestCase):
    """Test class for the user model."""
    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    @classmethod
    def setUpClass(cls):
        """Set up any necessary resources for the test cases."""
        try:
            os.rename('file.json', 'tmp.json')
            cls.name = 'User'
            cls.value = User
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
                user is created properly."""
        user_instance = self.value()
        self.assertEqual(type(user_instance), self.value)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs(self):
        """
        Test case to check if an instance of user\
                can be created with keyword arguments.
        """
        user_instance = self.value()
        copy = user_instance.to_dict()
        new = User(**copy)
        self.assertFalse(new is user_instance)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_int(self):
        """
        Test case to check if TypeError is raised when\
                creating user instance with integer keys.
        """
        user_instance = self.value()
        copy = user_instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = User(**copy)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_save(self):
        """Test case to check if the 'save' method saves \
                the user instance properly."""
        user_instance = self.value()
        user_instance.save()
        key = self.name + "." + user_instance.id
        with open('file.json', 'r') as f:
            objs = json.load(f)
            self.assertEqual(objs[key], user_instance.to_dict())

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_str(self):
        """Test case to check if the 'str' method returns\
                the expected string representation."""
        user_instance = self.value()
        self.assertEqual(str(user_instance),
                         '[{}] ({}) {}'.format(self.name,
                                               user_instance.id,
                                               user_instance.__dict__))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_todict(self):
        """Test case to check if the 'to_dict' method
                returns a dictionary representation of
                the user instance.
        """
        user_instance = self.value()
        n = user_instance.to_dict()
        self.assertEqual(user_instance.to_dict(), n)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_none(self):
        """Test case to check if TypeError is raised\
                when creating user instance with None keys."""
        none_dict = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**none_dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_id(self):
        """Test case to check the data type of the 'id' attribute."""
        user_instance = self.value()
        self.assertEqual(type(user_instance.id), str)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_created_at(self):
        """Test case to check the data\
                type of the 'created_at' attribute."""
        user_instance = self.value()
        self.assertEqual(type(user_instance.created_at), datetime)


class Test_user_DBStorage(unittest.TestCase):
    """Test class for the user model."""
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing FileStorage')
    @classmethod
    def setUpClass(cls):
        """
        setting up class
        """
        cls.storage = storage
        cls.storage.reload()

        cls.user = User(email="johnson@email.com",
                        password='johnson')

        cls.storage.new(cls.user)
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
        test class is_basemodel_subclass
        """
        self.assertIsInstance(self.user, BaseModel)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_email_attr(self):
        """
        test class email
        """
        self.assertTrue(hasattr(self.user, 'email'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_attr(self):
        """
        test class id attribute
        """
        self.assertTrue(hasattr(self.user, 'id'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_attr(self):
        """
        test class updated_at attribute
        """
        self.assertTrue(hasattr(self.user, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.user, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_first_name_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.user, 'first_name'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_last_name_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.user, 'last_name'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_places_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.user, 'places'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_reviews_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.user, 'reviews'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_first_name_value_none(self):
        """
        test class _first_name_value_none
        """
        self.assertEqual(self.user.first_name, None)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_last_name_value_none(self):
        """
        test class _last_name_value_none
        """
        self.assertEqual(self.user.last_name, None)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_value(self):
        """
        test class id
        """
        self.assertIsNotNone(self.user.id)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_value(self):
        """
        test class updated_at
        """
        self.assertIsNotNone(self.user.updated_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_value(self):
        """
        test class created_at
        """
        self.assertIsNotNone(self.user.created_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_first_name_with_value(self):
        """
        test class created_at
        """
        self.user.first_name = 'Johnson'
        self.assertEqual(self.user.first_name, "Johnson")

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_last_name_with_value(self):
        """
        test class created_at
        """
        self.user.last_name = 'Dennis'
        self.assertEqual(self.user.last_name, "Dennis")

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict(self):
        """
        test class created_at
        """
        self.assertEqual(type(self.user.to_dict()), dict)
        self.assertFalse('_sa_instance_user' in self.user.to_dict())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict_values(self):
        """
        test class created_at
        """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        class_name = self.user.to_dict().get('__class__')
        email = self.user.to_dict().get('email')
        created_at = self.user.to_dict().get('created_at')
        updated_at = self.user.to_dict().get('updated_at')
        places = self.user.to_dict().get('places')
        reviews = self.user.to_dict().get('reviews')

        self.assertEqual(class_name, 'User')
        self.assertEqual(type(email), str)
        self.assertEqual(created_at, self.user.created_at.strftime(t_format))
        self.assertEqual(updated_at, self.user.updated_at.strftime(t_format))
        self.assertEqual(places, [])
        self.assertEqual(reviews, [])

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_Base_subclass(self):
        """
        test that user is subclass of declarative base
        """
        self.assertIsInstance(self.user, Base)
        self.assertTrue('_sa_instance_state' in self.user.__dict__)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_str(self):
        """test that the str method has the correct output"""
        am_dict = self.user.__dict__
        am_dict.pop('_sa_instance_state')
        string = "[User] ({}) {}".format(self.user.id, am_dict)
        self.assertEqual(string, str(self.user))


if __name__ == '__main__':
    unittest.main()
