#!/usr/bin/python3
"""Module that tests the Review model."""
import os
import unittest
from datetime import datetime
import json
from models.review import Review
from models.place import Place
from models.user import User
from models.city import City
from models.state import State
from models.base_model import BaseModel, Base
from models import storage


STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class Test_Review_File_Storage(unittest.TestCase):
    """Test class for the review model."""
    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    @classmethod
    def setUpClass(cls):
        """Set up any necessary resources for the test cases."""
        try:
            os.rename('file.json', 'tmp.json')
            cls.name = 'Review'
            cls.value = Review
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
                review is created properly."""
        review_instance = self.value()
        self.assertEqual(type(review_instance), self.value)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs(self):
        """
        Test case to check if an instance of review\
                can be created with keyword arguments.
        """
        review_instance = self.value()
        copy = review_instance.to_dict()
        new = Review(**copy)
        self.assertFalse(new is review_instance)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_int(self):
        """
        Test case to check if TypeError is raised when\
                creating review instance with integer keys.
        """
        review_instance = self.value()
        copy = review_instance.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = Review(**copy)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_save(self):
        """Test case to check if the 'save' method saves \
                the review instance properly."""
        review_instance = self.value()
        review_instance.save()
        key = self.name + "." + review_instance.id
        with open('file.json', 'r') as f:
            objs = json.load(f)
            self.assertEqual(objs[key], review_instance.to_dict())

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_str(self):
        """Test case to check if the 'str' method returns\
                the expected string representation."""
        review_instance = self.value()
        self.assertEqual(str(review_instance),
                         '[{}] ({}) {}'.format(self.name,
                                               review_instance.id,
                                               review_instance.__dict__))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_todict(self):
        """Test case to check if the 'to_dict' method
                returns a dictionary representation of
                the review instance.
        """
        review_instance = self.value()
        n = review_instance.to_dict()
        self.assertEqual(review_instance.to_dict(), n)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_kwargs_none(self):
        """Test case to check if TypeError is raised\
                when creating review instance with None keys."""
        none_dict = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**none_dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_id(self):
        """Test case to check the data type of the 'id' attribute."""
        review_instance = self.value()
        self.assertEqual(type(review_instance.id), str)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing FileStorage')
    def test_created_at(self):
        """Test case to check the data\
                type of the 'created_at' attribute."""
        review_instance = self.value()
        self.assertEqual(type(review_instance.created_at), datetime)


class Test_review_DBStorage(unittest.TestCase):
    """Test class for the review model."""
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
        cls.review = Review(text='Beautiful',
                            place_id=cls.place.id,
                            user_id=cls.user.id)

        cls.storage.new(cls.state)
        cls.storage.new(cls.city)
        cls.storage.new(cls.user)
        cls.storage.new(cls.place)
        cls.storage.new(cls.review)
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
        self.assertIsInstance(self.review, BaseModel)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_name_attr(self):
        """
        test class name
        """
        self.assertTrue(hasattr(self.review, 'text'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_attr(self):
        """
        test class id attribute
        """
        self.assertTrue(hasattr(self.review, 'id'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_attr(self):
        """
        test class updated_at attribute
        """
        self.assertTrue(hasattr(self.review, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_attr(self):
        """
        test class created_at attribute
        """
        self.assertTrue(hasattr(self.review, 'created_at'))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_text_value_none(self):
        """
        test class name
        """
        self.assertNotEqual(self.review.text, None)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_id_value(self):
        """
        test class id
        """
        self.assertIsNotNone(self.review.id)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_updated_at_value(self):
        """
        test class updated_at
        """
        self.assertIsNotNone(self.review.updated_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_created_at_value(self):
        """
        test class created_at
        """
        self.assertIsNotNone(self.review.created_at)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_text_with_value(self):
        """
        test class created_at
        """
        self.assertTrue(self.review.text)
        self.assertEqual(self.review.text, "Beautiful")

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_place_id(self):
        """
        test class created_at
        """
        self.assertTrue(self.review.place_id)
        self.assertEqual(self.review.place_id, self.place.id)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_user_id(self):
        """
        test class created_at
        """
        self.assertTrue(self.review.user_id)
        self.assertEqual(self.review.user_id, self.user.id)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict(self):
        """
        test class created_at
        """
        self.assertEqual(type(self.review.to_dict()), dict)
        self.assertFalse('_sa_instance_state' in self.review.to_dict())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_to_dict_values(self):
        """
        test class created_at
        """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        class_name = self.review.to_dict().get('__class__')
        review_id = self.review.to_dict().get('id')
        review_text = self.review.to_dict().get('text')
        created_at = self.review.to_dict().get('created_at')
        updated_at = self.review.to_dict().get('updated_at')

        self.assertEqual(class_name, 'Review')
        self.assertEqual(type(review_id), str)
        self.assertEqual(type(review_text), str)
        self.assertEqual(created_at,
                         self.review.created_at.strftime(t_format))
        self.assertEqual(updated_at,
                         self.review.updated_at.strftime(t_format))

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_Base_subclass(self):
        """
        test that review is subclass of declarative base
        """
        self.assertIsInstance(self.review, Base)
        self.assertTrue('_sa_instance_state' in self.review.__dict__)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing DBStorage')
    def test_str(self):
        """test that the str method has the correct output"""
        am_dict = self.review.__dict__
        am_dict.pop('_sa_instance_state')
        string = "[Review] ({}) {}".format(self.review.id, am_dict)
        self.assertEqual(string, str(self.review))


if __name__ == '__main__':
    unittest.main()
