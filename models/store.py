from datetime import datetime
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # back_populates="items" is the same as "store" in ItemModel
    # lazy="dynamic" means that the items will not be loaded until we call .all()
    # This will speed up the query

    items = db.relationship(
        "ItemModel",
        back_populates="store",
        lazy="dynamic",
        cascade="all, delete",
    )

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(
            id=id
        ).first()  # SELECT * FROM stores WHERE id=id LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
