from flask import Flask,request,abort
import uuid
# from flask_smorest import
app = Flask(__name__)
from db import items,stores


# @app.get("/store")
# def get_stores():
#     return {"stores":stores}

#Stores

@app.route('/store', methods=['GET'])
def get_all_stores():
    return {"stores":list(stores.values())}

@app.route('/store', methods=['POST'])
def add_store():
    store_data=request.get_json()
    store_data=request.get_json()
    if(
        "name" not in store_data
    ):
        abort(400,"BAd request ")
    for store in stores.values():
        if(
            store["name"]==store_data["name"]
        ):
            abort(400 ,"store already exists ")
    store_id = uuid.uuid4().hex
    store={**store_data,"id":store_id}
    stores[store_id]=store
    return store,201

@app.route('/store/<string:store_id>', methods=['GET'])
def get_Store(store_id):
    try:
        return stores[store_id],201   
    except KeyError:
        abort(404,  "store not found")   

@app.route('/store/<string:store_id>',methods=["DELETE"])
def delete_Store(store_id):
    try:
        del stores[store_id]
        return {"message":"Store deleted"},201   
    except KeyError:
        abort(404,  "store not found")   



#Items

@app.route('/item', methods=['POST'])
def add_item_in_store():
    item_data=request.get_json()
    if(
        "price" not in item_data
        or "store_id"not in item_data
        or "name" not in item_data
    ):
        abort(400, "BAd request ")
    if item_data["store_id"] not in stores:
        abort(404,  "store not found")
    for item in items.values():
        if(
            item["name"]==item_data["name"]
            and item_data["store_id"]==item["store_id"]
        ):
            abort(400,  "item already exists ")
    item_id=uuid.uuid4().hex
    item={**item_data,"id":item_id}
    items[item_id]=item
    return item,201

@app.route('/item/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    try: 
        item_data=request.get_json()
        if(
            "price" not in item_data
            or "name" not in item_data
        ):
            abort(400, "BAd request ")
        item=items[item_id]
        item["price"]=item_data["price"]
        item["name"]=item_data["name"]
        return item,201
    except KeyError:
        abort(404,  "item not found")  

@app.route('/item', methods=['GET'])
def get_all_items():
    return {"items":list(items.values())},201
    
@app.route('/item/<string:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        return items[item_id],201   
    except KeyError:
        abort(404,  "item not found")   
    
@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Itrem deleted"}, 201   
    except KeyError:
        abort(404,  "item not found")   
    
