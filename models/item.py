from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer,db.ForeignKey('stores.id')) # Stablish just one store
    store =db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        self.name  = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name , 'price': self.price}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #SELECT * FROM item WHERE name=name LIMIT 1
                                                            # It returns an ItemModel object
#       Its also possible to pipe several filters
#       return ItemModel.query.filter_by(name=name).filter_by(id=1)
#       or
#        return ItemModel.query.filter_by(name=name,id=1)

    def save_to_db(self):        # Alchemy converts an object into a row, directly
        db.session.add(self) # You can add mutiple objects in a session and write it once
        db.session.commit()  # for efficiency purposes
                             # the add method uses the id, so you can use it
                             # for update or insert, so we rename insert method

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
