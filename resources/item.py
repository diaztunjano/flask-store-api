import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return "Item succesfully deleted", 200
        except KeyError:
            return abort(404, message="Item not found")

    def put(self, item_id):
        item_data = request.get_json()

        if "name" not in item_data or "price" not in item_data:
            return abort(400, message="Missing required fields ('name', 'price')")

        try:
            item = items[item_id]
        except KeyError:
            return abort(404, message="Item not found")

        item["name"] = item_data["name"]
        item["price"] = item_data["price"]

        return item, 200


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
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

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}

        items[item_id] = item

        return item, 201