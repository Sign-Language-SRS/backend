from flask import Blueprint
import logging

home_api = Blueprint('api', __name__)

@home_api.route("/")
def hello_world():
    logging.info("hello world")
    return "<p>Hello, World!</p>"
