#!/usr/bin/python3
"""
Unit tests for the Place model.
"""
import os
import unittest
import datetime
import json
from models.base_model import BaseModel, Base
from models.state import State
from models.user import User
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models import storage

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class TestPlace_FileStorage(unittest.TestCase):
    """
    Test class for the Place model.
    """
    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    @classmethod
    def setUpClass(cls):
        """
        Set up the class instance for the test
        """
        cls.storage = storage
        cls.storage.reload()
        cls.user = User()
        cls.state = State()
        cls.city = City(state_id=cls.state.id)
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name='House1')
        cls.review = Review(text="Greate place",
                            place_id=cls.place.id,
                            user_id=cls.user.id)
        cls.amenity = Amenity(name='WiFi')

        cls.place.amenity_ids.append(cls.amenity.id)
        cls.storage.new(cls.user)
        cls.storage.new(cls.state)
        cls.storage.new(cls.city)
        cls.storage.new(cls.place)
        cls.storage.new(cls.review)
        cls.storage.new(cls.amenity)
        cls.storage.save()
        try:
            os.rename('file.json', 'tmp.json')
        except Exception as exc:
            print(exc)
            pass

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    @classmethod
    def tearDownClass(cls):
        """
        teardown the class instance for the test
        """
        cls.storage.delete(cls.user)
        cls.storage.delete(cls.state)
        cls.storage.delete(cls.city)
        cls.storage.delete(cls.place)
        cls.storage.delete(cls.review)
        cls.storage.delete(cls.amenity)
        cls.storage.save()
        try:
            os.remove('file.json')
            os.rename('tmp.json', 'file.json')
        except Exception as exc:
            print(exc)
            pass

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_place_id(self):
        """
        Test case to check the data type of the 'place_id'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.id), str)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_place_city_id_is_str(self):
        """
        Test case to check the data type of the 'place_id'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.city_id), str)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_place_name_is_str(self):
        """
        Test case to check the data type of the 'place_id'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.name), str)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_place_user_id_is_str(self):
        """
        Test case to check the data type of the 'place_id'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.user_id), str)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_name(self):
        """
        Test case to check the data type of the 'name'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.name), str)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_description(self):
        """
        Test case to check the data type of the 'description'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.description), str)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_number_rooms(self):
        """
        Test case to check the data type of the 'number_rooms'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.number_rooms), int)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_number_bathrooms(self):
        """
        Test case to check the data type of the 'number_bathrooms
          attribute in the Place model.
        """
        self.assertEqual(type(self.place.number_bathrooms), int)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_max_guest(self):
        """
        Test case to check the data type of the 'max_guest'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.max_guest), int)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_price_by_night(self):
        """
        Test case to check the data type of the 'price_by_night'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.price_by_night), int)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_latitude(self):
        """
        Test case to check the data type of the 'latitude'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.latitude), float)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_longitude(self):
        """
        Test case to check the data type of the 'longitude'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.longitude), float)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_amenity_ids(self):
        """
        Test case to check the data type of the 'amenity_ids'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.amenity_ids), list)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_review(self):
        """
        Test case to check the value type of the 'reviews'
        attribute in the Place model.
        """
        self.assertTrue(hasattr(self.place, 'reviews'))

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_city_id_with_value(self):
        """
        Test case to check the data type of the 'city_id'
        attribute in the Place model.
        """
        self.assertEqual(self.place.city_id, self.city.id)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_user_id_with_value(self):
        """
        Test case to check the data type of the 'user_id'
        attribute in the Place model.
        """
        self.assertEqual(self.place.user_id, self.user.id)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_str(self):
        """Test case to check if the 'str' method returns\
                the expected string representation."""
        place_dict = self.place.__dict__.copy()
        place_dict.pop('_sa_instance_state')
        self.assertEqual(str(self.place),
                         '[{}] ({}) {}'.format(self.place.__class__.__name__,
                                               self.place.id,
                                               place_dict))


class TestPlace_DBStorage(unittest.TestCase):
    """
    Test for dbstorage
    """
    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    @classmethod
    def setUpClass(cls):
        """
        setup for dbstorage test
        """
        cls.storage = storage
        cls.storage.reload()
        cls.user = User(email='Johnson@email.com', password='johnson')
        cls.state = State(name='Nairobi')
        cls.city = City(name='City-1', state_id=cls.state.id)
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name='House1')
        cls.review = Review(text="Greate place",
                            place_id=cls.place.id,
                            user_id=cls.user.id)
        cls.amenity = Amenity(name='WiFi')

        cls.place.amenities.append(cls.amenity)
        cls.storage.new(cls.user)
        cls.storage.new(cls.state)
        cls.storage.new(cls.city)
        cls.storage.new(cls.place)
        cls.storage.new(cls.review)
        cls.storage.new(cls.amenity)
        cls.storage.save()

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    @classmethod
    def tearDownClass(cls):
        """
        teardown for dbstorage test
        """
        cls.storage.close()

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_place_id(self):
        """
        Test case to check the data type of the 'place_id'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.id), str)
        self.assertTrue(self.place.id)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_place_city_id_is_str(self):
        """
        Test case to check the data type of the 'place_id'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.city_id), str)
        self.assertIsNotNone(self.place.city_id)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_place_name_is_str(self):
        """
        Test case to check the data type of the 'place_id'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.name), str)
        self.assertIsNotNone(self.place.name)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_place_user_id_is_str(self):
        """
        Test case to check the data type of the 'place_id'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.user_id), str)
        self.assertIsNotNone(self.place.user_id)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_name(self):
        """
        Test case to check the data type of the 'name'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.name), str)
        self.assertIsNotNone(self.place.name)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_description(self):
        """
        Test case to check the data type of the 'description'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.description), str)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_number_rooms(self):
        """
        Test case to check the data type of the 'number_rooms'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.number_rooms), int)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_number_bathrooms(self):
        """
        Test case to check the data type of the 'number_bathrooms
          attribute in the Place model.
        """
        self.assertEqual(type(self.place.number_bathrooms), int)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_max_guest(self):
        """
        Test case to check the data type of the 'max_guest'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.max_guest), int)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_price_by_night(self):
        """
        Test case to check the data type of the 'price_by_night'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.price_by_night), int)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_latitude(self):
        """
        Test case to check the data type of the 'latitude'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.latitude), float)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_longitude(self):
        """
        Test case to check the data type of the 'longitude'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.longitude), float)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_amenity_ids(self):
        """
        Test case to check the data type of the 'amenity_ids'
        attribute in the Place model.
        """
        self.assertEqual(type(self.place.amenity_ids), list)
        self.assertIsNotNone(self.place.amenities)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_review(self):
        """
        Test case to check the value type of the 'reviews'
        attribute in the Place model.
        """
        self.assertTrue(hasattr(self.place, 'reviews'))
        self.assertIsNotNone(self.place.reviews)

    @unittest.skipIf(STORAGE_TYPE != 'db', 'Testing FileSTorage')
    def test_city_id_with_value(self):
        """
        Test case to check the data type of the 'city_id'
        attribute in the Place model.
        """
        self.assertEqual(self.place.city_id, self.city.id)

    @unittest.skipIf(STORAGE_TYPE or STORAGE_TYPE == 'db',
                     'Testing DBSTorage')
    def test_user_id_with_value(self):
        """
        Test case to check the data type of the 'user_id'
        attribute in the Place model.
        """
        self.assertEqual(self.place.user_id, self.user.id)


if __name__ == '__main__':
    unittest.main()
