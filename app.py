import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.route("/store", methods=["GET", "POST"])
def create_store():
    store_data = request.get_json()

    if "name" not in store_data:
        return abort(400, message="Missing required fields ('name')")

    for store in stores.values():
        if store["name"] == store_data["name"]:
            return abort(400, message="Store already exists")

    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store

    return new_store, 201


@app.route("/stores", methods=["GET"])
def get_stores():
    return {"stores": list(stores.values())}


@app.route("/stores/<string:store_id>", methods=["GET"])
def get_store(store_id):
    try:
        return stores[int(store_id)]
    except KeyError:
        return abort(404, message="Store not found")


@app.route("/item", methods=["GET", "POST"])
def create_item():
    item_data = request.get_json()

    if (
        "name" not in item_data
        or "price" not in item_data
        or "store_id" not in item_data
    ):
        return abort(
            400, message="Missing required fields ('name', 'price', 'store_id')"
        )

    for item in items.values():
        if (
            item["name"] == item_data["name"]
            and item["store_id"] == item_data["store_id"]
        ):
            return abort(400, message="Item already exists in store")

    if item_data["store_id"] not in stores:
        return abort(404, message="Store not found")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}

    items[item_id] = item

    return item, 201


@app.route("/items", methods=["GET"])
def get_items():
    return {"items": list(items.values())}


@app.route("/items/<string:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return abort(404, message="Item not found")
