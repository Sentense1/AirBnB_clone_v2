#!/usr/bin/python3
"""Defines the City class."""
from os import getenv
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

STORAGE_TYPE = getenv("HBNB_TYPE_STORAGE")


if STORAGE_TYPE and STORAGE_TYPE == "db":
    class City(BaseModel, Base):
        """Represents a city for a MySQL database.

        Inherits from SQLAlchemy Base and links to the MySQL table cities.

        Attributes:
            __tablename__ (str): The name of the MySQL table to store Cities.
            name (sqlalchemy String): The name of the City.
            state_id (sqlalchemy String): The state id of the City.
        """
        __tablename__ = "cities"

        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"),
                          nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="all, delete-orphan")
if not STORAGE_TYPE or STORAGE_TYPE != 'db':
    class City(BaseModel):
        """Represents a city for a MySQL database.

        Inherits from SQLAlchemy Base and links to the MySQL table cities.

        Attributes:
            __tablename__ (str): The name of the MySQL table to store Cities.
            name (sqlalchemy String): The name of the City.
            state_id (sqlalchemy String): The state id of the City.
        """
        state_id = ""
        name = ""
