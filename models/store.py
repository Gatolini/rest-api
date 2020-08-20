from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
# stablish there is a list (one to many)
    items = db.relationship('ItemModel',lazy='dynamic')
# whenever we create an store model, we are going to go and create
# an object for each item
# lazy='dynamic', to tell SQLAlchemy do not go into the items table and create
# an object for each item yet

    def __init__(self,name):
        self.name  = name

# we have to use the .all() method, to avoid an error
# so, until we use the json method, we are not looking into table (due to lazy)
# so, creating a stores is very simple, but every time we call the json method
# we are going to the table. It is going to be slower
    def json(self):
        return {'name': self.name , 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
