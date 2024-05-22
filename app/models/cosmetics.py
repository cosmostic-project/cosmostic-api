from uuid import uuid4

from extensions import cosmetics_db


CATEGORIES = ('hats', 'backpacks', 'body', 'head', 'others')

class Cape(cosmetics_db.Document):
    uuid = cosmetics_db.UUIDField(binary=False, default=lambda:uuid4(), unique=True)
    name = cosmetics_db.StringField(min_length=2, max_length=16, required=True, unique=True)
    author = cosmetics_db.StringField(min_length=2, max_length=16, required=True)
    texture = cosmetics_db.ImageField(required=True, size=(46, 22, True))
    preview = cosmetics_db.ImageField(required=True, size=(10, 16, True))

    meta = {'db_alias': 'default', 'collection': 'capes'}

class Accessory(cosmetics_db.Document):
    uuid = cosmetics_db.UUIDField(binary=False, default=lambda:uuid4(), unique=True)
    name = cosmetics_db.StringField(min_length=2, max_length=16, required=True, unique=True)
    author = cosmetics_db.StringField(min_length=2, max_length=16, required=True)
    model = cosmetics_db.DictField(required=True)
    texture = cosmetics_db.ImageField(required=False, size=(46, 22, True))
    category = cosmetics_db.StringField(required=True, default=None, choices=CATEGORIES)
    preview = cosmetics_db.ImageField(required=True, size=(150, 150, True))

    meta = {'db_alias': 'default', 'collection': 'accessories'}