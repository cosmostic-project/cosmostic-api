from flask_restx import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import mongoengine


api = Api()
cors = CORS()
jwt = JWTManager()
# Dbs
users_db = mongoengine
cosmetics_db = mongoengine