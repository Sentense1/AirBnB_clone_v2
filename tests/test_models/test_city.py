#!/usr/bin/python3
"""
Unit tests for the City model.
"""

from tests.test_models.test_base_model import Test_Basemodel
from models.city import City


class test_City(Test_Basemodel):
    """
    Test class for the City model.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """
        Test case to check the data type of \
                the 'state_id' attribute in the City model.
        """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """
        Test case to check the data type of \
                the 'name' attribute in the City model.
        """
        new = self.value()
        self.assertEqual(type(new.name), str)
