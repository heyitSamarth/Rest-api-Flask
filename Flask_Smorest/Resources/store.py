import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from db import stores
from Schemas import StoreSchema

blp =Blueprint("stores",__name__,description="Operations on stores")


@blp.route("/store")
class Store(MethodView):
    @blp.response(201,StoreSchema(many=True))
    def get (self):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):
        for store in stores.values():
            if(
                store["name"]==store_data["name"]
            ):
                abort(400 ,message="store already exists ")
        store_id = uuid.uuid4().hex
        store={**store_data,"id":store_id}
        stores[store_id]=store
        return store


@blp.route("/store/<string:store_id>")
class StoreList(MethodView):
    @blp.response(201,StoreSchema)
    def get (self,store_id):
        try:
            return stores[store_id],201   
        except KeyError:
            abort(404,  message="store not found")   
    
    def delete(self,store_id):
        try:
            del stores[store_id]
            return {"message":"Store deleted"},201   
        except KeyError:
            abort(404,  message="store not found")  