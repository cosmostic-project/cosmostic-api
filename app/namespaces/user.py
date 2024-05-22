from flask import current_app, request
from flask_restx import Resource, Namespace

from extensions import api
from parsers import user_cape_parser, user_accessory_parser
from models.users import User
from models.cosmetics import Cape, Accessory
from utils import mojang
from utils.commons import create_response
from utils.decorators import ensure_uuid_match, check_uuid
from authorizations import bearer_token


authorizations = {
    "JWT" : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization'
    }
}
user = Namespace("user", description="Manage user cosmetics", path="/user", authorizations=bearer_token)


@user.route('/<string:user_uuid>/cape', doc={
    'responses': {
        404: 'User not found',
        400: 'Invalid user uuid'
    }
})
class CapeSettings(Resource):  
    @api.doc(responses={200: 'Success', 422: 'No active cape'})
    @check_uuid
    def get(self, user_uuid:str):
        """
        Get active cape
        """
        # check if user exist
        user = User.objects(minecraft_uuid=user_uuid).first()
        if not user:
            return create_response(404, "User not found or not registered")

        # check if user has active cape
        cape = user.cape
        if not cape:
            return create_response(422, "No active cape")

        return create_response(200, data=str(cape.uuid))
    
    @user.expect(user_cape_parser)
    @api.doc(responses={200: 'Updated', 201: 'Created', 404: 'Cape not found'})
    @api.doc(security="BearerToken")
    @check_uuid
    @ensure_uuid_match
    def put(self, user_uuid:str):
        """
        Update user active cape
        """
        # get args
        args = user_cape_parser.parse_args()

        # check if cape exists
        cape = Cape.objects(uuid=args.cape_uuid).first()
        if not cape:
            return create_response(404, "Cape not found")

        # check if user exist
        user = User.objects(minecraft_uuid=user_uuid).first()
        if not user:
            # check if user uuid exist (mojang account)
            if not mojang.get_profile(user_uuid):
                return create_response(404, "User doesn't exist")
            
            user = User(minecraft_uuid=user_uuid, cape=cape).save()   # create new user
            return create_response(201, "Created")
        
        # update user active cape
        user.cape = cape
        user.save()

        current_app.logger.info(f"{request.remote_addr} - ({user_uuid}) Updated his active cape to {args.cape_uuid}")
        return create_response(200, "Updated")
    
    @api.doc(responses={200: 'Deleted', 422: 'No active cape'})
    @api.doc(security="BearerToken")
    @check_uuid
    @ensure_uuid_match
    def delete(self, user_uuid:str):
        """
        Remove active cape
        """
        # check if user exist
        user = User.objects(minecraft_uuid=user_uuid).first()
        if not user:
            return create_response(404, "User not found or not registered")
        
        # check if user has active cape
        cape = user.cape
        if not cape:
            return create_response(422, "No active cape")

        # remove active cape
        user.cape = None
        user.save()

        current_app.logger.info(f"{request.remote_addr} - ({user_uuid}) Removed his active cape")
        return create_response(200, "Removed")


@user.route('/<string:user_uuid>/accessories', doc={
    'responses': {
        400: 'Invalid user uuid',
        404: 'User not found',
        422: 'No active accessories'
    }
})
class AccessoriesSettings(Resource):
    @api.doc(responses={200: 'Success'})
    @check_uuid
    def get(self, user_uuid:str):
        """
        Get list of active accessories
        """
        # check if user exist
        user = User.objects(minecraft_uuid=user_uuid).first()
        if not user:
            return create_response(404, "User not found or not registered")
        
        # check if user has active accessories
        accessories = user.accessories
        if not accessories:
            return create_response(422, "No active accessories")
            
        response = [accessory.uuid for accessory in accessories]

        return create_response(200, data=response)
    
    @user.expect(user_accessory_parser)
    @api.doc(responses={200: 'Added', 409: 'Accessory already active', 404: 'Accessory not found', 403: 'Too many accessories'})
    @api.doc(security="BearerToken")
    @check_uuid
    @ensure_uuid_match
    def post(self, user_uuid:str):
        """
        Add accessory
        """
        # get args
        args = user_accessory_parser.parse_args()

        # check if accessory exists
        accessory = Accessory.objects(uuid=args.accessory_uuid).first()
        if not accessory:
            return create_response(404, "Accessory not found")

        # check if user exist
        user = User.objects(minecraft_uuid=user_uuid).first()
        if not user:
            # check if user uuid exist (mojang account)
            if not mojang.get_profile(user_uuid):
                return create_response(404, "User doesn't exist")
            
            user = User(minecraft_uuid=user_uuid, accessories=[accessory]).save()   # create new user
            return create_response(201, "Created")
        
        if accessory in user.accessories:   # check if accessory already active
            return create_response(409, "Accessory already active")
        
        # check if too many accessories
        if len(user.accessories) >= 5:
            return create_response(403, "Too many accessories")

        # update user active cape
        user.accessories.append(accessory)
        user.save()

        current_app.logger.info(f"{request.remote_addr} - ({user_uuid}) Added accessory {args.accessory_uuid} to active")
        return create_response(200, "Added")
    
    @user.expect(user_accessory_parser)
    @api.doc(responses={200: 'Removed', 404: 'Accessory not found'})
    @api.doc(security="BearerToken")
    @check_uuid
    @ensure_uuid_match
    def delete(self, user_uuid:str):
        """
        Delete specified accessory
        """
        # get args
        args = user_accessory_parser.parse_args()
        
        # check if user exist
        user = User.objects(minecraft_uuid=user_uuid).first()
        if not user:
            return create_response(404, "User not found or not registered")
        
        # check if user have accessory
        accessory = next((accessory for accessory in user.accessories if accessory.uuid == args.accessory_uuid), None)
        if not accessory:
            return create_response(404, "Accessory not active")
        
        # remove accessory
        user.accessories.remove(accessory)
        user.save()
        
        current_app.logger.info(f"{request.remote_addr} - ({user_uuid}) Removed accessory {args.accessory_uuid} from active")
        return create_response(200, "Removed")