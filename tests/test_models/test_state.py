#!/usr/bin/python3
"""
Unit tests for the State model.
"""

from tests.test_models.test_base_model import Test_Basemodel
from models.state import State


class test_state(Test_Basemodel):
    """
    Test class for the State model.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the test class."""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """
        Test case to check the data type of the
        'name' attribute in the State model.
        """
        new = self.value()
        self.assertEqual(type(new.name), str)
