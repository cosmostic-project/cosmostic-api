from extensions import users_db
from .cosmetics import Cape, Accessory


class User(users_db.Document):
    minecraft_uuid = users_db.UUIDField(binary=False, required=True, unique=True)
    cape = users_db.ReferenceField(Cape, reverse_delete_rule=users_db.CASCADE, required=False)
    accessories = users_db.ListField(users_db.ReferenceField(Accessory, reverse_delete_rule=users_db.CASCADE, required=False))

    meta = {'db_alias': 'users_db', 'collection': 'users'}