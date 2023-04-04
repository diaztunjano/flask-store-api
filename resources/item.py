from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from flask_jwt_extended import get_jwt, jwt_required

from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            item = ItemModel.find_by_id(item_id)
            return item
        except SQLAlchemyError:
            abort(500, message="An error occurred while retrieving the item.")

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            abort(403, message="You are not authorized to perform this action.")
        try:
            item = ItemModel.find_by_id(item_id)
            item.delete_from_db()
            return {"message": "Item deleted."}
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the item.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = ItemModel.find_by_id(item_id)
            if item:
                item.name = item_data["name"]
                item.price = item_data["price"]
            else:
                item = ItemModel(id=item_id, **item_data)

            item.save_to_db()
            return item
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating the item.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            return ItemModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while retrieving the items.")

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        print(item_data)
        item = ItemModel(**item_data)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
