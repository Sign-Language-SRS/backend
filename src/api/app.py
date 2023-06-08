# logic for starting and configuring the application itself
from flask import Flask
from flask_migrate import Migrate
from api.config import Config
import logging

# blueprints
from api.route.home import home_api

def create_app():
    app = Flask(__name__)
    # config magic    
    app.config.from_object(Config)

    # database migrations stuff
    from api.models import db
    db.init_app(app)
    # migrations
    migrate = Migrate(app, db)

    # blueprints
    app.register_blueprint(home_api, url_prefix='/')
    return app

def add_logging_to_file(filename='srs.log', log_level=logging.INFO):
    logging.basicConfig(filename=filename, level=log_level)
