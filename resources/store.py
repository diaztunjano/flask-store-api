from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import StoreModel
from schemas import ItemSchema, StoreSchema


blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            store = StoreModel.find_by_id(store_id)
            return store
        except SQLAlchemyError:
            abort(500, message="An error occurred while retrieving the store.")

    def delete(self, store_id):
        try:
            store = StoreModel.find_by_id(store_id)
            store.delete_from_db()
            return {"message": "Store deleted."}
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the store.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        try:
            return StoreModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while retrieving the stores.")

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            store.save_to_db()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store_data
