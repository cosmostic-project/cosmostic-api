from flask_restx import reqparse

from utils import validator


# user cape parser
user_cape_parser = reqparse.RequestParser()
user_cape_parser.add_argument('cape_uuid', type=validator.uuid, required=True, help="Cape uuid")

# user accessory parser
user_accessory_parser = reqparse.RequestParser()
user_accessory_parser.add_argument('accessory_uuid', type=validator.uuid, required=True, help="Accessory uuid")

### manage cape parsers
# create cape parser
create_cape_parser = reqparse.RequestParser()
create_cape_parser.add_argument('cape_name', type=validator.string, required=True, help="Cape name")
create_cape_parser.add_argument('cape_texture', type=validator.cape_texture, required=True, location='files', help="Cape texture")
create_cape_parser.add_argument('author', type=validator.string, required=True, help="Cape author")
# update cape parser
update_cape_parser = reqparse.RequestParser()
update_cape_parser.add_argument('cape_uuid', type=validator.uuid, required=True, help="Cape uuid")
update_cape_parser.add_argument('cape_name', type=validator.string, required=False, help="New cape name")
update_cape_parser.add_argument('cape_texture', type=validator.cape_texture, required=False, location='files', help="New cape texture")
update_cape_parser.add_argument('author', type=validator.string, required=False, help="New cape author")
# delete cape parser
delete_cape_parser = reqparse.RequestParser()
delete_cape_parser.add_argument('cape_uuid', type=validator.uuid, required=True, help="Cape uuid")

## manage accessory parsers
# create accessory parser
create_accessory_parser = reqparse.RequestParser()
create_accessory_parser.add_argument('accessory_name', type=validator.string, required=True, help="Accessory name")
create_accessory_parser.add_argument('accessory_model', type=validator.accessory_model, required=True, help="Accessory model")
create_accessory_parser.add_argument('accessory_category', type=validator.string, required=True, help="Accessory category")
create_accessory_parser.add_argument('accessory_texture', type=validator.accessory_texture, required=False, location='files', help="Accessory texture")
create_accessory_parser.add_argument('accessory_preview', type=validator.accessory_preview, required=True, location='files', help="Accessory preview")
create_accessory_parser.add_argument('author', type=validator.string, required=True, help="Accessory author")
# update accessory parser
update_accessory_parser = reqparse.RequestParser()
update_accessory_parser.add_argument('accessory_uuid', type=validator.uuid, required=True, help="Accessory uuid")
update_accessory_parser.add_argument('accessory_name', type=validator.string, required=False, help="New accessory name")
update_accessory_parser.add_argument('accessory_model', type=validator.accessory_model, required=False, help="New accessory model")
update_accessory_parser.add_argument('accessory_category', type=validator.string, required=False, help="New accessory category")
update_accessory_parser.add_argument('accessory_texture', type=validator.accessory_texture, required=False, location='files', help="New accessory texture")
update_accessory_parser.add_argument('accessory_preview', type=validator.accessory_preview, required=False, location='files', help="Accessory preview")
update_accessory_parser.add_argument('author', type=validator.string, required=False, help="New accessory author")
# delete accessory parser
delete_accessory_parser = reqparse.RequestParser()
delete_accessory_parser.add_argument('accessory_uuid', type=validator.uuid, required=True, help="Accessory uuid")