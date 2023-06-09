from datetime import datetime
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # back_populates="store" is the same as "items" in StoreModel
    store = db.relationship("StoreModel", back_populates="items")
    # secondary="items_tags" is the same as "tags" in TagModel
    tags = db.relationship("TagModel", secondary="items_tags", back_populates="items")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(
            id=id
        ).first()  # SELECT * FROM items WHERE id=id LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
