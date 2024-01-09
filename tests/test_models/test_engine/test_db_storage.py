#!/usr/bin/python3
"""
Containing the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """updted with the MySQL """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiating aDBStorage obj"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """adding the obj"""
        self.__session.add(obj)

    def save(self):
        """commit the current database """
        self.__session.commit()

    def delete(self, obj=None):
        """ option delete"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """database reloading"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """remove methode calling"""
        self.__session.remove()

    def get(self, cls, id):
        """query """
        if cls:
            obj = self.__session.query(cls).get(id)
            return obj
        return None

    def count(self, cls=None):
        """Returns the num of obj in storage"""
        if cls:
            all_objs_dict = self.all(cls)
            count = len(all_objs_dict)
        else:
            count = len(self.all())
        return count
