from flask import Blueprint
import logging

home_api = Blueprint('api', __name__)

@home_api.route("/")
def hello_world():
    logging.info("hello world")
    return "<p>Hello, World!</p>"

# @app.route("/get_reviews")
# @connection_decorator
# def get_reviews_route(conn):
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM card WHERE card.next_review <= NOW()")
#     reviews = cur.fetchall()
#     conn.commit()
#     cur.close()
#     return reviews

