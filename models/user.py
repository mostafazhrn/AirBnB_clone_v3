#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib
from hashlib import md5


class User(BaseModel, Base):
    """THis shall create a Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """This instant shall initializes user"""
        if 'pass' in kwargs:
            passwd = kwargs['pass']
            hsh = hashlib.md5()
            hsh.update(str(passwd).encode('utf-8'))
            kwargs['pass'] = hsh.hexdigest()
        super().__init__(*args, **kwargs)
