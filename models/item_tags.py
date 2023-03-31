from db import db


class ItemTags(db.Model):
    # This table is used to create a many-to-many relationship between items and tags
    __tablename__ = "items_tags"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable=False)
