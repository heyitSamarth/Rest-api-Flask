import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort #Divide api in multiple segments
from db import stores

blp =Blueprint("stores",__name__,description="Operations on stores")


@blp.route("/store")
class Store(MethodView):
    def get (self):
        return {"stores":list(stores.values())}  
    def post(self):
        store_data=request.get_json()
        if(
            "name" not in store_data
        ):
            abort(400,message="Bad request ")
        for store in stores.values():
            if(
                store["name"]==store_data["name"]
            ):
                abort(400 ,message="store already exists ")
        store_id = uuid.uuid4().hex
        store={**store_data,"id":store_id}
        stores[store_id]=store
        return store,201 


@blp.route("/store/<string:store_id>")
class StoreList(MethodView):
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