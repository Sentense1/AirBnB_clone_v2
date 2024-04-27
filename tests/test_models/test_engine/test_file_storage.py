#!/usr/bin/python3
""" Mdule to test file_storage """
import os
import unittest
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class TestFileStorage(unittest.TestCase):
    """
    Unit tests for the FileStorage class.
    """

    @unittest.skipIf(STORAGE_TYPE == 'db',
                     'Testing DBStorage')
    def setUp(self):
        """Set up the test environment."""
        try:
            os.rename('file.json', 'tmp.json')
        except Exception:
            pass
        self.del_list = []
        for key in storage._FileStorage__objects.keys():
            self.del_list.append(key)

    @unittest.skipIf(STORAGE_TYPE == 'db',
                     'Testing DBStorage')
    def tearDown(self):
        """Remove storage file at the end of tests."""
        try:
            os.rename('tmp.json', 'file.json')
            for key in self.del_list:
                del storage._FileStorage__objects[key]
        except Exception:
            pass

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_obj_list_empty(self):
        """Test that __objects is initially empty."""
        self.assertEqual(len(storage.all()), 0)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_new(self):
        """Test that a new object is correctly added to __objects."""
        new = BaseModel()
        for obj in storage.all().values():
            self.assertTrue(new is obj)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_all(self):
        """Test that __objects is properly returned."""
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_base_model_instantiation(self):
        """Test that a file is not created on BaseModel save."""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_new_state(self):
        """Test that a new object is correctly added to __objects."""
        new = State(name='California')
        for obj in storage.all().values():
            self.assertTrue(new is obj)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_all_state(self):
        """Test that __objects is properly returned."""
        new = State(name='California')
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_state_model_instantiation(self):
        """Test that a file is not created on state save."""
        new = State(name='California')
        self.assertFalse(os.path.exists('file.json'))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_new_city(self):
        """Test that a new object is correctly added to __objects."""
        state = State(name='California')
        new = City(state_id=state.id)
        for obj in storage.all().values():
            self.assertTrue(new is obj)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_all_city(self):
        """Test that __objects is properly returned."""
        state = State(name='California')
        new = City(state_id=state.id)
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_city_model_instantiation(self):
        """Test that a file is not created on city save."""
        state = State(name='California')
        city = City(state_id=state.id)
        self.assertFalse(os.path.exists('file.json'))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_new_place(selfj):
        """Test that a new object is correctly added to __objects."""
        state = State(name='California')
        city = City(state_id=state.id)
        place = Place(city_id=city.id, name='House1')
        for obj in storage.all().values():
            self.assertTrue(place is obj)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_all_place(self):
        """Test that __objects is properly returned."""
        state = State(name='California')
        city = City(state_id=state.id)
        place = Place(city_id=city.id, name='House1')
        temp = storage.all(place)
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_place_model_instantiation(self):
        """Test that a file is not created on place save."""
        state = State(name='California')
        city = City(state_id=state.id)
        place = Place(city_id=city.id, name='House1')
        self.assertFalse(os.path.exists('file.json'))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_new_review(self):
        """Test that a new object is correctly added to __objects."""
        state = State(name='California')
        city = City(state_id=state.id)
        user = User(email='email@email.com', password='password')
        place = Place(city_id=city.id, name='House1')
        review = Review(text='wonderful', user_id=user.id, place_id=place.id)
        for obj in storage.all().values():
            self.assertTrue(review is obj)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_all_review(self):
        """Test that __objects is properly returned."""
        state = State(name='California')
        city = City(state_id=state.id)
        user = User(email='email@email.com', password='password')
        place = Place(city_id=city.id, name='House1')
        review = Review(text='wonderful', user_id=user.id, place_id=place.id)
        temp = storage.all(Review)
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_review_model_instantiation(self):
        """Test that a file is not created on place save."""
        state = State(name='California')
        city = City(state_id=state.id)
        user = User(email='email@email.com', password='password')
        place = Place(city_id=city.id, name='House1')
        review = Review(text='wonderful', user_id=user.id, place_id=place.id)
        self.assertFalse(os.path.exists('file.json'))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_new_amenity(self):
        """Test that a new object is correctly added to __objects."""
        amenity = Amenity(name='WIFI')
        for obj in storage.all().values():
            self.assertTrue(amenity is obj)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_all_amenity(self):
        """Test that __objects is properly returned."""
        amenity = Amenity(name='wifi')
        temp = storage.all(Amenity)
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_amenity_model_instantiation(self):
        """Test that a file is not created on place save."""
        amenity = Amenity(name='wifi')
        self.assertFalse(os.path.exists('file.json'))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_empty(self):
        """Test that data is saved to the file."""
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_save(self):
        """Test the FileStorage save method."""
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_reload(self):
        """Test that the storage file is successfully loaded to __objects."""
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            self.assertEqual(new.to_dict()['id'], obj.to_dict()['id'])

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_reload_empty(self):
        """Test loading from an empty file."""
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_reload_from_nonexistent(self):
        """Test that nothing happens if the file does not exist."""
        self.assertEqual(storage.reload(), None)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_base_model_save(self):
        """Test that BaseModel's save method calls the storage save."""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_type_path(self):
        """Test that __file_path is a string."""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_type_objects(self):
        """Test that __objects is a dictionary."""
        self.assertEqual(type(storage.all()), dict)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_key_format(self):
        """Test that the key is properly formatted."""
        for key in self.del_list:
            del storage._FileStorage__objects[key]
        new = BaseModel()
        new_key = f'BaseModel.{new.to_dict()}'
        for key, value in storage.all().items():
            self.assertEqual(key, new_key)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'Testing DBStorage')
    def test_storage_var_created(self):
        """Test that the storage object is created."""
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)


if __name__ == '__main__':
    unittest.main()
