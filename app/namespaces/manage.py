from flask import current_app, request
from flask_restx import Resource, Namespace
from flask_jwt_extended import get_jwt_identity
from mongoengine import NotUniqueError, ValidationError

from extensions import api
from parsers import (
    create_cape_parser,
    update_cape_parser,
    delete_cape_parser,
    create_accessory_parser,
    update_accessory_parser,
    delete_accessory_parser
)
from models.cosmetics import Cape, Accessory
from utils.commons import create_cape_preview, create_response
from utils.decorators import ensure_admin
from authorizations import bearer_token


manage = Namespace("manage", description="Manage cosmetics", path="/manage", authorizations=bearer_token)


@manage.route('/cape')
class CapeManagement(Resource):
    @manage.expect(create_cape_parser)
    @api.doc(responses={200: 'Created', 409: 'Cape name already used'})
    @api.doc(security="BearerToken")
    @ensure_admin
    def post(self):
        """
        Create new cape
        """
        # get args
        args = create_cape_parser.parse_args()

        cape_preview = create_cape_preview(args.cape_texture)   # create cape preview

        try:
            # create new cape
            Cape(name=args.cape_name, author=args.author, texture=args.cape_texture, preview=cape_preview).save()
        except NotUniqueError as e:
            return create_response(409, "Cape name already used")

        current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Created new cape : {args.cape_name}")
        return create_response(200, "Created")

    @manage.expect(update_cape_parser)
    @api.doc(responses={200: 'Updated', 404: 'Cape not found'})
    @api.doc(security="BearerToken")
    @ensure_admin
    def put(self):
        """
        Update cape informations
        """
        # get args
        args = update_cape_parser.parse_args()

        cape = Cape.objects(uuid=args.cape_uuid).first()
        if not cape:
            return create_response(404, "Cape not found")

        # update cape informations if specified
        cape.name = args.cape_name or cape.name
        cape.author = args.author or cape.author

        if args.cape_texture:
            cape.texture = args.cape_texture
            cape.preview = create_cape_preview(args.cape_texture)   # update cape preview

        try:
            cape.save()
        except NotUniqueError:
            return create_response(409, "Cape name already used")

        current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Updated {args.cape_uuid} cape informations : {[k for k, v in args.items() if v is not None and k != 'cape_uuid']}")
        return create_response(200, "Updated")
    
    @manage.expect(delete_cape_parser)
    @api.doc(responses={200: 'Deleted', 404: 'Cape not found'})
    @api.doc(security="BearerToken")
    @ensure_admin
    def delete(self):
        """
        Delete specified cape
        """
        # get args
        args = delete_cape_parser.parse_args()

        cape = Cape.objects(uuid=args.cape_uuid).first()
        if not cape:
            return create_response(404, "Cape not found")

        cape.delete()

        current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Deleted {args.cape_uuid} cape")
        return create_response(200, "Deleted")


@manage.route('/accessory')
class AccessoryManagement(Resource):
    @manage.expect(create_accessory_parser)
    @api.doc(responses={200: 'Created', 409: 'Accessory name already used', 400: "Accessory category doesn't exist"})
    @api.doc(security="BearerToken")
    @ensure_admin
    def post(self):
        """
        Create new accessory
        """
        # get args
        args = create_accessory_parser.parse_args()
        
        try:
            # create new cape
            Accessory(name=args.accessory_name, author=args.author, texture=args.accessory_texture, category=args.accessory_category, model=args.accessory_model, preview=args.accessory_preview).save()
        except NotUniqueError:
            return create_response(409, "Accessory name already used")
        except ValidationError:
            return create_response(400, "Accessory category doesn't exist")

        current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Created new accessory : {args.accessory_name}")
        return create_response(200, "Created")

    @manage.expect(update_accessory_parser)
    @api.doc(responses={200: 'Updated', 404: 'Accessory not found', 400: "Accessory category doesn't exist"})
    @api.doc(security="BearerToken")
    @ensure_admin
    def put(self):
        """
        Update accessory informations
        """
        # get args
        args = update_accessory_parser.parse_args()

        accessory = Accessory.objects(uuid=args.accessory_uuid).first()
        if not accessory:
            return create_response(404, "Accessory not found")

        # update accessory informations if specified
        accessory.name = args.accessory_name or accessory.name
        accessory.author = args.author or accessory.author
        accessory.texture = args.accessory_texture or accessory.texture
        accessory.model = args.accessory_model or accessory.model
        accessory.category = args.accessory_category or accessory.category
        accessory.preview = args.accessory_preview or accessory.preview

        try:
            accessory.save()
        except NotUniqueError as e:
            return create_response(409, "Accessory name already used")
        except ValidationError as e:
            return create_response(400, "Accessory category doesn't exist")

        current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Updated {args.accessory_uuid} accessory informations : {[k for k, v in args.items() if v is not None and k != 'accessory_uuid']}")
        return create_response(200, "Updated")
    
    @manage.expect(delete_accessory_parser)
    @api.doc(responses={200: 'Deleted', 404: 'Accessory not found'})
    @api.doc(security="BearerToken")
    @ensure_admin
    def delete(self):
        """
        Delete specified accessory
        """
        # get args
        args = delete_accessory_parser.parse_args()

        accessory = Accessory.objects(uuid=args.accessory_uuid).first()
        if not accessory:
            return create_response(404, "Accessory not found")

        accessory.delete()

        current_app.logger.info(f"{request.remote_addr} - ({get_jwt_identity()}) Deleted {args.accessory_uuid} accessory")
        return create_response(200, "Deleted")