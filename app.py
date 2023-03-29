from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "TheStore",
        "items": [
            {"name": "Chair", "price": 14.5},
            {"name": "Table", "price": 30},
            {"name": "Ladder", "price": 5},
        ],
    }
]


@app.route("/stores", methods=["GET"])
def get_stores():
    return {"stores": stores}


@app.route("/store", methods=["GET", "POST"])
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)

    return new_store, 201


@app.route("/store/<string:name>/item", methods=["GET", "POST"])
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


@app.route("/stores/<string:name>", methods=["GET"])
def get_specific_store(name):
    for store in stores:
        if store["name"] == name:
            return {"store": store}
    return {"message": "Store not found"}, 404


@app.route("/stores/<string:name>/items", methods=["GET"])
def get_specific_store_items(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
