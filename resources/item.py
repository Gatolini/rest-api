from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# Resource as things that the API responds with
# ot things that the Client can ask for
# API deals with Resources as users, items, stores, students
# a resource is the external representation of an entity
# ========================================================
# a Model is an internal representation of an entity
# ====================================================
#  Example:
#    user = User.find_by_username(username)
# in this case, we are using the Model, not the Resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type = float,
            required = True,
            help = "This field can not left blank"
     )
    parser.add_argument('store_id',
            type = float,
            required = True,
            help = "Every item needs a store id."
     )

    @jwt_required()
    def get(self, name):
        # The code is segregated to a separate method
        # to reuse it

        item = ItemModel.find_by_name(name)
        if item:
        #    return item # is an object
            return item.json()
        return {'message':"No such item {}".format(name)},404

    def post(self, name):
        # data = request.get_json(force=True) # you dont need the content type header
                                              # even if the header is not aplication/json
        # data = request.get_json(silent=True) # it does not give an error
                                               # it basically returns none
        ## replaced by find_by_name call
        ## if next(filter(lambda x:x['name'] == name, items),None):
         # the default is not None, so you can omit to specify is not None
        if ItemModel.find_by_name(name):
            return {'Message':"Item '{}' does already exists".format(name)},400

        data = Item.parser.parse_args()
        # initial
        # item = ItemModel(name,data['price'],data['store_id']) # now, is an object
        # can be simplified
        item = ItemModel(name,**data)

        ## items.append(item)

        try:
            item.save_to_db()
        except:
            return {'message':'An error ocurred inserting the item'},500 # Internal server error
        # return item, 201 # created
        return item.json(), 201 # created
                                # 202 accepted - the creation was delayed

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message' : 'item deleted'}

    def put(self,name): # this is idempotent. If exists, update,
                        # if not, then create

        data = Item.parser.parse_args() # is going to parse, and put the only valid data

        item = ItemModel.find_by_name(name)

        if item is None:
            # intial
            # item = ItemModel(name, data['price'],data['store_id'])
            # simplified
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        # lambda is a better option
        # On the other hand, instructor suggest to use map, only if the people
        # is using other languages like javascrip
        return {'items': list(map(lambda x: x.json, ItemModel.query.all()))}
#        first option: list comprehension
#        return {'items': [item.json() for item in ItemModel.query.all()]}
