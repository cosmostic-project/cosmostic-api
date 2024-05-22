from flask import send_file, url_for, make_response
from flask_restx import Resource, Namespace
from io import BytesIO

from models.cosmetics import Cape, Accessory
from utils.commons import create_response
from utils.decorators import check_uuid


fetch = Namespace("fetch", description="Fetch cosmetics resources", path="/fetch")


@fetch.route('/capes', doc={
    'responses': {200: 'Success'}
})
class ListCapes(Resource):
    def get(self):
        """
        List all capes
        """
        # get cape list
        capes = Cape.objects()
        
        response = []
        for cape in capes:
            response.append(cape.uuid)
        
        return create_response(200, data=response)


@fetch.route('/cape/<string:cape_uuid>', doc={
    'responses': {
        200: 'Success',
        400: 'Invalid cape uuid',
        404: 'Cape uuid not found'
    }
})
class CapeInformations(Resource):
    @check_uuid
    def get(self, cape_uuid:str):
        """
        Fetch cape informations
        """
        # get cape informations from db
        cape = Cape.objects(uuid=cape_uuid).first()
        if not cape:
            return create_response(404, "Cape not found")

        response = {
            'uuid': cape.uuid,
            'name': cape.name,
            'author': cape.author,
            'texture': url_for('fetch_cape_texture', cape_uuid=cape.uuid),
            'preview': url_for('fetch_cape_preview', cape_uuid=cape.uuid)
        }

        return create_response(200, data=response)


@fetch.route('/cape/<string:cape_uuid>/texture', doc={
    'responses': {
        200: 'Success',
        400: 'Invalid cape uuid',
        404: 'Cape uuid not found'
    }
})
class CapeTexture(Resource):
    @check_uuid
    def get(self, cape_uuid:str):
        """
        Fetch cape image
        """    
        # get cape informations from db
        cape = Cape.objects(uuid=cape_uuid).first()
        if not cape:
            return create_response(404, "Cape not found")

        image = BytesIO(cape.texture.read())

        return make_response(send_file(image, mimetype='image/png', download_name=f"{cape.uuid}.png"), 200)
    

@fetch.route('/cape/<string:cape_uuid>/preview', doc={
    'responses': {
        200: 'Success',
        400: 'Invalid cape uuid',
        404: 'Cape uuid not found'
    }
})
class CapePreview(Resource):
    @check_uuid
    def get(self, cape_uuid:str):
        """
        Fetch cape preview image
        """
        # get cape informations from db
        cape = Cape.objects(uuid=cape_uuid).first()
        if not cape:
            return create_response(404, "Cape not found")

        image = BytesIO(cape.preview.read())

        return make_response(send_file(image, mimetype='image/png', download_name=f"{cape.uuid}.png"), 200)


@fetch.route('/accessories', doc={
    'responses': {200: 'Success'}
})
class ListAccessories(Resource):
    def get(self):
        """
        List all accessories
        """
        # get accessory list
        accessories = Accessory.objects()
        
        response = []
        for accessory in accessories:
            response.append(accessory.uuid)
        
        return create_response(200, data=response)


@fetch.route('/accessory/<string:accessory_uuid>', doc={
    'responses': {
        200: 'Success',
        400: 'Invalid accessory uuid',
        404: 'Accessory uuid not found'
    }
})
class AccessoryInformations(Resource):
    @check_uuid
    def get(self, accessory_uuid:str):
        """
        Fetch accessory informations
        """
        # get accessory informations from db
        accessory = Accessory.objects(uuid=accessory_uuid).first()
        if not accessory:
            return create_response(404, "Accessory not found")
        
        response = {
            'uuid': accessory.uuid,
            'name': accessory.name,
            'author': accessory.author,
            'category': accessory.category,
            'preview': url_for('fetch_accessory_preview', accessory_uuid=accessory.uuid),
            'texture': url_for('fetch_accessory_texture', accessory_uuid=accessory.uuid) if accessory.texture else None
        }

        return create_response(200, data=response)


@fetch.route('/accessory/<string:accessory_uuid>/texture', doc={
    'responses': {
        200: 'Success',
        400: 'Invalid accessory uuid',
        404: 'Accessory uuid not found'
    }
})
class AccessoryTexture(Resource):
    @check_uuid
    def get(self, accessory_uuid:str):
        """
        Fetch accessory texture
        """    
        # get accessory informations from db
        accessory = Accessory.objects(uuid=accessory_uuid).first()
        if not accessory:
            return create_response(404, "Accessory not found")

        image = accessory.texture.read()

        if not image:
            return create_response(404, "Accessory doesn't have texture")

        image = BytesIO(image)

        return make_response(send_file(image, mimetype='image/png', download_name=f"{accessory.uuid}.png"), 200)


@fetch.route('/accessory/<string:accessory_uuid>/preview', doc={
    'responses': {
        200: 'Success',
        400: 'Invalid accessory uuid',
        404: 'Accessory uuid not found'
    }
})
class AccessoryPreview(Resource):
    @check_uuid
    def get(self, accessory_uuid:str):
        """
        Fetch accessory preview image
        """
        # get accessory informations from db
        accessory = Accessory.objects(uuid=accessory_uuid).first()
        if not accessory:
            return create_response(404, "Accessory not found")

        image = BytesIO(accessory.preview.read())

        return make_response(send_file(image, mimetype='image/png', download_name=f"{accessory.uuid}.png"), 200)


@fetch.route('/accessory/<string:accessory_uuid>/model', doc={
    'responses': {
        200: 'Success',
        400: 'Invalid accessory uuid',
        404: 'Accessory uuid not found'
    }
})
class AccessoryModel(Resource):
    @check_uuid
    def get(self, accessory_uuid:str):
        """
        Fetch accessory model
        """
        # get accessory informations from db
        accessory = Accessory.objects(uuid=accessory_uuid).first()
        if not accessory:
            return create_response(404, "Accessory not found")

        return create_response(200, data=accessory.model)