import sqlite3
from db import db

# Class User is not a Resource, because the API cannot receive
# data into this class or send this class as a JSON representation
# User is a helper that we use to store some data and contains
# some methods that allow us to easily retrive User objects from
# a database
# a Model is an internal representation of an entity
# ====================================================
# a resource is the external representation of an entity
# ========================================================
#  Example:
#    user = User.find_by_username(username)
# in this case, we are using the Model, not the Resource

class UserModel(db.Model):
    # defintion of the table and its columns
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    # usually, the columns matches the properties in the constructor
    # but if not, the remaining properties are ignored, without any error

    def __init__(self,username,password):
# id is python keyword, so _id. self.id is fine...
# I assume it is distinguishable
#       self.id = _id
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()

# In fact, this is an API (not a REST API), Exposes two endpoints, these two methods
# are an interface for other parts of our programm to interact with the user thing
# For example, Security uses the endpointo to interact with User
