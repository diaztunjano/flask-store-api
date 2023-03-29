import uuid
from flask import Flask, request
from db import items, stores

app = Flask(__name__)


@app.route("/stores", methods=["GET"])
def get_stores():
    return {"stores": list(stores.values())}


@app.route("/store", methods=["GET", "POST"])
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store

    return new_store, 201


@app.route("/item", methods=["GET", "POST"])
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}

    items[item_id] = item

    return item, 201


@app.route("/items", methods=["GET"])
def get_all_items():
    return {"items": list(items.values())}


@app.route("/stores/<string:store_id>", methods=["GET"])
def get_specific_store(store_id):
    try:
        return stores[int(store_id)]
    except KeyError:
        return {"message": "Store not found"}, 404


@app.route("/items/<string:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404
