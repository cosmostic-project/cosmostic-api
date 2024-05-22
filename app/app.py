from flask import Flask, render_template, request
import logging.config
import yaml

from extensions import api, users_db, cosmetics_db, cors, jwt
from namespaces import fetch, user, manage
from errors_handling import handler
from settings import Config
from utils import validator


# load logging config
with open('logging.yml') as config:
    LOGGING_CONFIG = yaml.safe_load(config.read())


def create_app():
    """
    Creates and configures the Flask API application.

    Returns:
    app: configured Flask application.
    """
    # configure logging
    logging.getLogger("werkzeug").disabled = True   # disable werkzeug default logging
    logging.config.dictConfig(LOGGING_CONFIG)

    # create app
    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.debug("Config loaded")
    
    app.config['BUNDLE_ERRORS'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    
    # check admin list
    admins = app.config.get('ADMINS')
    if not admins:
        app.logger.warning("Admin list is empty")
    else:
        try:
            app.config['ADMINS'] = [validator.uuid(admin) for admin in admins]   # check if uuids are valid
        except:
            raise ValueError('Invalid admin list : check uuids validity')

    # init extensions
    api.init_app(app, title='COSMOSTIC API', description='COSMOSTIC Internal API', version='1.0')
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/fetch/*": {"origins": "*", "methods": ["GET"]},
        r"/user/*": {"origins": "*", "methods": ["GET"]}
    })

    users_db.connect(db='users', alias='users_db', host=app.config['USERS_DB_URI'], serverSelectionTimeoutMS=app.config['MONGO_TIMEOUT'])
    cosmetics_db.connect(db='cosmetics', alias='default', host=app.config['COSMETICS_DB_URI'], serverSelectionTimeoutMS=app.config['MONGO_TIMEOUT'])

    # namespaces registration
    api.add_namespace(fetch)
    api.add_namespace(user)
    api.add_namespace(manage)
    
    app.register_blueprint(handler)   # error handling blueprint

    # documentation endpoint
    @api.documentation
    def swaggerui():
        """
        Custom Swagger UI endpoint.

        Returns:
        Response: The rendered Swagger UI page.
        """
        return render_template('swaggerui.html')

    # requests logging
    @app.after_request
    def log_requests(response):
        app.logger.info(f"{request.remote_addr} - [{request.method}] {request.url} | {response.status_code}")
        return response

    app.logger.debug("App created")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()