import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return "Store succesfully deleted", 200
        except KeyError:
            return abort(404, message="Store not found")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
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