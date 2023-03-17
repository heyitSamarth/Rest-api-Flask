from flask import Flask,request
import uuid
app = Flask(__name__)
from db import items,stores


# @app.get("/store")
# def get_stores():
#     return {"stores":stores}

@app.route('/store', methods=['GET'])
def get_stores():
    return {"stores":list(stores.values())}

@app.route('/store', methods=['POST'])
def add_store():
    store_data=request.get_json()
    store_id = uuid.uuid().hex
    store={**store_data,"id":store_id}
    stores.append(store)
    return store,201

@app.route('/store/<string:store_name>/item', methods=['POST'])
def add_item_in_store(store_name):
    request_data=request.get_json()
    for store in stores:
        if(store["name"]==store_name):
            new_item={ "name":request_data["name"],"price":request_data["price"]}
            store["items"].append(new_item)
            return new_item,201
    return {"message":"store not found"},404

@app.route('/store/<string:store_id>', methods=['GET'])
def method_name(store_id):
    try:
        return stores[store_id],201   
    except KeyError:
        return {"message":"store not found"},404    
    

# if __name__ == '__main__':
#     app.run()
