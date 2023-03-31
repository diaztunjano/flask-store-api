from datetime import datetime
from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", secondary="items_tags", back_populates="tags")

    def __init__(self, name, store_id):
        self.name = name
        self.store_id = store_id

    def json(self):
        return {"name": self.name}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
