from flask import Blueprint, jsonify, request
from api.models import db
from api.models.reviews import Deck, Card
import logging

reviews_api = Blueprint('reviews', __name__)

@reviews_api.route("/decks", methods=["GET", "POST", "UPDATE"])
def get_decks():
  if request.method == "POST":
    # handle creating a new deck
    return 200

  if request.method == "GET":
    decks = Deck.query.all()
    return jsonify(decks)
  
  return 400

@reviews_api.route("/decks/<int:deck_id>/reviews", methods=["GET"])
def get_reviews(deck_id):
  if request.method == "GET":
    reviews = Card.query.filter()
    deck = Deck.query.filter(Deck.id == deck_id).first()
    return jsonify(deck)
