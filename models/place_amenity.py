#!/usr/bin/python3
"""
Sqlalchemy Module for place0amenity
"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import Base


class PlaceAmenity(Base):
    """Represents the many-to-many relationship between places and amenities.

    Attributes:
        place_id (Column, Integer): Foreign key referencing the place.id column.
        amenity_id (Column, Integer): Foreign key referencing the amenity.id column.
    
    """
    __tablename__ = 'place_amenity'
    place_id =  Column(String(60), ForeignKey("places.id"), primary_key=True, nullable=False)
    amenity_id = Column( String(60), ForeignKey("amenities.id"),
                        primary_key=True, nullable=False)
