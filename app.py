from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
# a folder is a package, if it contains a file named __init__.py
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db
from resources.store import Store, StoreList

# On import, we dont want to do things
# that we only want to do when we run the file

app = Flask(__name__)
# the database location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # lives in the same directory
# this turn off the flask SQLAlchemy modification tracker
# It does not turn off the SQLAlchemy modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

# this decorator comes directly from flask
# it is like a activation registry
@app.before_first_request
def create_tables():
    db.create_all() # it will only create the tables that it sees (through the import)

jwt = JWT(app, authenticate, identity) # creates a new end point
                                       # /auth
api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

# Only the file that is run is __main__ (i.e. pyhon app.py)
# one way to avoid undesiderable actions is to use an if
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug = True)
