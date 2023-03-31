from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # dump_only=True means that the field will be included in the response but not in the request
    id = fields.String(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class ItemUpdateSchema(Schema):
    name = fields.String()
    price = fields.Float()


class ItemSchema(PlainItemSchema):
    # Whenever we use ItemSchema, we will also get the store field
    store_id = fields.Integer(required=True, load_only=True)
    # This will be used when returing data to the client
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
