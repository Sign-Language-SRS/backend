# logic for starting and configuring the application itself
from flask import Flask, url_for
from flask_migrate import Migrate
from api.config import Config
import logging

# blueprints
from api.route.home import home_api
from api.route.reviews import reviews_api

# swagger documentation
from flask_swagger_ui import get_swaggerui_blueprint

def create_app():
    app = Flask(__name__)
    # config magic    
    app.config.from_object(Config)

    # database migrations stuff
    from api.models import db
    db.init_app(app)

    # migrations
    import api.models.reviews
    migrate = Migrate(app, db)

    # blueprints
    app.register_blueprint(home_api, url_prefix='/')
    app.register_blueprint(reviews_api, url_prefix='/api/v1/')
    
    # swagger stuff
    SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
    API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "SRS Sign Language Backend"
        }
    )

    app.register_blueprint(swaggerui_blueprint)
    return app

def add_logging_to_file(filename='srs.log', log_level=logging.INFO):
    logging.basicConfig(filename=filename, level=log_level)
