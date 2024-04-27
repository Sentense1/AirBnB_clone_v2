#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import object_session


class DBStorage:
    """Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.

        If cls is None, queries all types of objects.

        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        objs = []
        if not cls:
            for subclass in Base.__subclasses__():
                objs.extend(self.__session.query(subclass).all())
        else:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError as e:
                    print('cls not mapped to Base: ', e)
                    pass
            if cls in Base.__subclasses__():
                objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj:
            self.__session.delete(obj)

    def objs_in_session(self, obj):
        """
        Shows all objects in section
        """
        if not obj:
            print('no obj passed')
            return
        # get all objects in sqlalchemy session
        all_objects = self.__session.identity_map.values()
        # iterate through all objects in session
        for ob in all_objects:
            # check if each object is an instance of declarative base
            if isinstance(obj, Base) and ob == obj:
                # print the objects in session
                return f'object name: "{type(obj).__name__}" still in session'

    def obj_in_session(self, obj):
        """
        Shows if the specified object is in the session.
        """
        if not obj:
            print('No object passed')
            return

        # Check if the object is associated with a session
        sess = object_session(obj)
        # Check if the object's id is in the session's identity_map
        sess_id_map = self.__session.identity_map.get(type(obj), obj.id)
        # print('sess_id_map: ', sess_id_map)
        # output = sess_id_map:  5e7b84bf-0493-4859-9cf0-c539acb54c67

        if sess and sess_id_map:
            return f'Object name: "{type(obj).__name__}" is still in session'
        else:
            return f'Object name: "{type(obj).__name__}" is not in session'

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()

    def reload2(self):
        """
        Create all tables in the database and initialize a new session.
        """
        # connects to the database using engine object and retrieves
        # existing table information
        Base.metadata.reflect(self.__engine)
        # the retrieved table information is stored in Base.metadata.tables
        # which is a dictionary

        # checks if tables are created already
        if not Base.metadata.tables:
            # create tables if tables are not created
            Base.metadata.create_all(self.__engine)
        else:
            print("Tables already exist, not recreating")

        # creates a new session factory bound to the engine
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        # The expire_on_commit=False parameter means that the session
        # will not expire after each commit.

        # creates a new scoped session object from the session factory
        Session = scoped_session(session_factory)
        # A scoped session is a thread-local session that is automatically
        # cleaned up after each request.

        # creates a new session object from the scoped session object and
        # assigns it to the __session attribute of the current object
        self.__session = Session()
        # This session object is used to interact with the database.

        # By including session in the reload method, we ensure that the session
        # object is always up-to-date and ready to use after the tables have
        # been reflected and created if necessary.
