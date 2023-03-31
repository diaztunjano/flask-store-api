from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<string:store_id>/tag")
class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        try:
            store = StoreModel.find_by_id(store_id)
            return store.tags.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while retrieving the store's tags.")

    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self, tag_data, store_id):
        try:
            tag = TagModel(**tag_data, store_id=store_id)
            tag.save_to_db()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        try:
            tag = TagModel.find_by_id(tag_id)
            return tag
        except SQLAlchemyError:
            abort(500, message="An error occurred while retrieving the tag.")
