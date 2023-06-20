from flask import Blueprint, jsonify, request
from api.models import db
from api.models.reviews import Deck, Card
from api.models.inputs import ReviewInput, NewDeckInput
import logging, datetime

reviews_api = Blueprint('reviews', __name__)

@reviews_api.route("/decks", methods=["GET", "POST"])
def get_decks():
  if request.method == "POST":
    """
    handle creating a new deck
    input: 
    {
      name: <string>
    }
    """

    # handle creating a new deck
    input_json = request.get_json()
    try:
      new_deck = NewDeckInput(input_json)
    except:
      print("misformed review input")
      return "error", 400

    new_deck.add_deck()
    return "success", 200
  if request.method == "GET":
    decks = Deck.query.all()
    return jsonify(decks)
  return "error", 400

@reviews_api.route("/decks/<int:deck_id>/reviews", methods=["GET", "POST"])
def handle_reviews(deck_id):
  if request.method == "GET":
    cards = Card.query.filter(Card.deck_id == deck_id, Card.next_review <= datetime.datetime.now()).all()
    return jsonify(cards)
  elif request.method == "POST":
    # in this case, we do validation on the frontend, lets users also decide for themselves whether it's right or not
    """
    handle getting the reviews
    input: vector of the following
    {
      card_id: <int>,
      correct: <bool>
    }

    if it's correct, we update the card
    TODO: Add logging to reviews
    """

    input_json = request.get_json()
    try:
      input_reviews = [ReviewInput(input) for input in input_json]
    except:
      print("misformed review input")
      return "error", 400
    
    # now that we've got a correct array of ReviewInput structs
    # we can go through each of them and verify that it's valid to update
    # and update them if it is
    output = []

    for review in input_reviews:
      if review.verify_timestamp():
        if review.handle_review():
          output.append(
            Card.query.filter(Card.id == review.card_id).first()
          )

    return jsonify(output)

@reviews_api.route("/decks/<int:deck_id>/cards", methods=["GET"])
def get_cards_from_deck(deck_id):
  if request.method == "GET":
    deck = Deck.query.filter(Deck.id == deck_id).first()
    # grab cards
    cards = Card.query.filter(Card.deck_id == deck.id).all()
    return jsonify(cards)
  if request.method == "POST":
    # adds in a card to a deck
    pass

@reviews_api.route("/decks/<int:deck_id>/cards/<int:card_id>", methods=["GET"])
def get_single_card_from_deck(deck_id, card_id):
  if request.method == "GET":
    deck = Deck.query.filter(Deck.id == deck_id).first()
    # grab cards
    cards = Card.query.filter(Card.deck_id == deck.id and Card.id == card_id).first()
    return jsonify(cards)
