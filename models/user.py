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
        super().__init__(*args, **kwargs)

    def __setattr__(self, nom, valu):
        """ This shall convert passwd to md5 hash"""
        if nom == 'password':
            self.password = md5(valu.encode()).hexdigest()
        else:
            setattr(self, nom, valu)
