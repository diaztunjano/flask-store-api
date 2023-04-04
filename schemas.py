from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    # dump_only=True means that the field will be included in the response but not in the request
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class PlainTagSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)


class ItemUpdateSchema(Schema):
    name = fields.String()
    price = fields.Float()
    store_id = fields.Integer()


class ItemSchema(PlainItemSchema):
    # Whenever we use ItemSchema, we will also get the store field
    store_id = fields.Integer(required=True, load_only=True)
    # This will be used when returing data to the client
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Integer(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class TagAndItemSchema(Schema):
    message = fields.String()
    tag = fields.Nested(TagSchema)
    item = fields.Nested(ItemSchema)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
