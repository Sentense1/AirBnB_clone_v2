#!/usr/bin/python3
""" Module for testing db_storage """
import os
import unittest
from unittest.mock import patch
from io import StringIO
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.db_storage import DBStorage

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class TestDBStorage(unittest.TestCase):
    """Unit tests for the DBStorage class."""
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing FileStorage')
    @classmethod
    def setUpClass(cls) -> None:
        cls.storage = DBStorage()
        cls.storage.reload()
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.user = User(email="test@example.com", password="password")
        cls.place = Place(name="Cozy Apartment", city_id=cls.city.id, user_id=cls.user.id)
        cls.review = Review(text="Great place!", place_id=cls.place.id,
                        user_id=cls.user.id)
        cls.amenity = Amenity(name="WiFi")
        cls.place.amenities.append(cls.amenity)
        cls.storage.new(cls.state)
        cls.storage.new(cls.city)
        cls.storage.new(cls.user)
        cls.storage.new(cls.place)
        cls.storage.new(cls.review)
        cls.storage.new(cls.amenity)
        cls.storage.save()

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     'Testing FileStorage')
    @classmethod
    def tearDown(cls) -> None:
        cls.storage.close()

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all(self):
        """
        Test the all() method of DBStorage.
        """
        all_objs = self.storage.all()
        self.assertEqual(all_objs[f"State.{self.state.id}"], self.state)
        self.assertEqual(all_objs[f"City.{self.city.id}"], self.city)
        self.assertEqual(all_objs[f"User.{self.user.id}"], self.user)
        self.assertEqual(all_objs[f"Place.{self.place.id}"], self.place)
        self.assertEqual(all_objs[f"Review.{self.review.id}"], self.review)
        self.assertEqual(all_objs[f"Amenity.{self.amenity.id}"], self.amenity)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(self.storage.all()), dict)

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all_state(self):
        """
        Test the all() method of DBStorage.
        """
        all_state = self.storage.all('State')
        print(all_state)
        state_id = f'{self.state.__class__.__name__}.{self.state.id}'
        self.assertIn(state_id, all_state)
    
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all_city(self):
        """
        Test the all() method of DBStorage.
        """
        all_city = self.storage.all('City')
        city_id = f'{self.city.__class__.__name__}.{self.city.id}'
        self.assertIn(city_id, all_city)
    
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all_user(self):
        """
        Test the all() method of DBStorage.
        """
        all_user = self.storage.all('User')
        user_id = f'{self.user.__class__.__name__}.{self.user.id}'
        self.assertIn(user_id, all_user)
    
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all_place(self):
        """
        Test the all() method of DBStorage.
        """
        all_place = self.storage.all('Place')
        place_id = f'{self.place.__class__.__name__}.{self.place.id}'
        self.assertIn(place_id, all_place)
    
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all_review(self):
        """
        Test the all() method of DBStorage.
        """
        all_review = self.storage.all('Review')
        review_id = f'{self.review.__class__.__name__}.{self.review.id}'
        self.assertIn(review_id, all_review)
    
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all_amenity(self):
        """
        Test the all() method of DBStorage.
        """
        all_amenity = self.storage.all('Amenity')
        amenity_id = f'{self.amenity.__class__.__name__}.{self.amenity.id}'
        self.assertIn(amenity_id, all_amenity)
    
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_all_place_amenity(self):
        """
        Test the all() method of DBStorage.
        """
        all_place = self.storage.all('Place').values()
        for value in all_place:
            amenities: list = value.to_dict().get('amenities')
            for am in amenities:
                self.assertEqual(self.amenity.id, am.to_dict().get('id'))

    # @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
    #                  "Testing FILEStorage")
    # def test_delete_without_obj(self):
    #     """
    #     Test the test_delete_without_obj method of DBStorage.
    #     """
    #     self.assertIn(f"State.{self.state.id}", self.storage.all())

    #     # Test delete() with obj=None
    #     self.storage.delete()
    #     self.storage.save()
    #     self.assertIn(f"State.{self.state.id}", self.storage.all().keys())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_delete_place(self):
        """Test the delete() method of DBStorage."""
        all_am = self.storage.all('Amenity')
        for am in all_am.values():
            if self.amenity == am:
                print('am in amenity: ', am, '\n', '\n')
                self.storage.delete(am)
        all_place = self.storage.all('Place').values()
        for place in all_place:
            if self.place == place:
                for am in self.place.amenities:
                    print('before: ', am)
                    self.storage.delete(am)
                    print('after: ', am)
                    self.storage.delete(self.place)
                    self.storage.save()
        self.assertNotIn(f"Place.{self.place.id}", self.storage.all())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_delete_city(self):
        """Test the delete() method of DBStorage."""

        self.storage.delete(self.city)
        self.storage.save()
        self.assertNotIn(f"City.{self.city.id}", self.storage.all())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_delete_state(self):
        """Test the delete() method of DBStorage."""
        self.storage.delete(self.state)
        self.storage.save()
        self.assertNotIn(f"State.{self.state.id}", self.storage.all())

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_delete_user(self):
        """Test the delete() method of DBStorage."""

        self.storage.delete(self.user)
        self.storage.save()
        self.assertNotIn(f"User.{self.user.id}", self.storage.all())

    # @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
    #                  "Testing FILEStorage")
    # def test_close(self):
    #     """Test the close() method of DBStorage."""
    #     self.storage.close()
    #     self.assertIsNone(self.storage._DBStorage__session)

class TestDBStorageNewSaveReload(unittest.TestCase):
    """
    Tests for storage.save, new and reload methods
    """
    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_new(self):
        """test that new adds an object to the database"""
        pass

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_save(self):
        """Test that save properly saves objects to database"""
        pass

    @unittest.skipIf(not STORAGE_TYPE or STORAGE_TYPE != 'db',
                     "Testing FILEStorage")
    def test_reload(self):
        """Test the reload() method of DBStorage."""
        storage = DBStorage()
        storage.reload()
        state = State(name="Nairobi")
        storage.new(state)
        storage.save()

        num_of_obj_before = len(storage.all())
        print('num_of_obj_before: ', num_of_obj_before)

        storage.reload()

        num_of_obj_after =  len(storage.all())
        print('num_of_obj_after :', num_of_obj_after)

        self.assertEqual(num_of_obj_before, 1)
        self.assertEqual(num_of_obj_after, 0)


if __name__ == '__main__':
    unittest.main()
