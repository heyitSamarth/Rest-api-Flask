import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from db import items,stores
from Schemas import ItemSchema,ItemUpdateSchema

blp =Blueprint("items",__name__,description="Operations on items")

@blp.route("/item/<string:item_id>")
class ItemList(MethodView):

    @blp.response(200,ItemSchema)
    def get (self,item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message= "item not found") 
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201,ItemSchema)
    def put (self,item_data,item_id):
        try: 
            item=items[item_id]
            item["price"]=item_data["price"]
            item["name"]=item_data["name"]
            return item,201
        except KeyError:
            abort(404,  "item not found")  
    
    def delete(self,item_id):
        try:
            del items[item_id]
            return {"message":"Itrem deleted"}, 201   
        except KeyError:
            abort(404,  message="item not found")   

@blp.route("/item")
class Item(MethodView):
    
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        if item_data["store_id"] not in stores:
            abort(404, message= "store not found")
        for item in items.values():
            if(
                item["name"]==item_data["name"]
                and item_data["store_id"]==item["store_id"]
            ):
                abort(400,  message="item already exists ")
        item_id=uuid.uuid4().hex
        item={**item_data,"id":item_id}
        items[item_id]=item
        return item
