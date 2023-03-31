from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import TagModel, StoreModel
from models.item import ItemModel
from schemas import TagAndItemSchema, TagSchema

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

    @blp.response(
        202,
        description="Deletes a tag if no item is linked to it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is linked to one or more items. In this case, the tag cannot be deleted.",
    )
    def delete(self, tag_id):
        try:
            tag = TagModel.find_by_id(tag_id)
            if not tag.items:
                tag.delete_from_db()
                return {"message": "Tag deleted."}
            abort(400, message="Tag is linked to one or more items.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting the tag.")
        return tag


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItems(MethodView):
    @blp.response(201, TagSchema)
    def post(self, tag_id, item_id):
        tag = TagModel.find_by_id(tag_id)
        item = ItemModel.find_by_id(item_id)
        item.tags.append(tag)
        try:
            item.save_to_db()

        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, tag_id, item_id):
        try:
            tag = TagModel.find_by_id(tag_id)
            item = ItemModel.find_by_id(item_id)
            item.tags.remove(tag)
            item.save_to_db()

        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag
