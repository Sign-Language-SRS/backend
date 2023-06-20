from api.models import db
from dataclasses import dataclass
from api.models.reviews import Card, Bin, BinTypeEnum, Deck
import datetime

@dataclass
class ReviewInput():
    card_id: int
    correct: bool

    def __init__(self, input: dict):
        if ("card_id" not in input and "correct" not in input):
            raise Exception("misformed review input")
        self.card_id = input["card_id"]
        self.correct = input["correct"]

    # handles the review itself
    def handle_review(self) -> bool:
        card = Card.query.filter(Card.id == self.card_id).first()
        bin = card.get_bin()
        
        # initializing the bin to use later
        next_bin: Bin

        if self.correct:
            # if they passed it, grab the necessary info, then update it
            # check if it's a last bin, in which case we just stop
            if bin.bin_type == BinTypeEnum.end_bin:
                return False

            next_bin = Bin.query.filter(Bin.id == bin.correct_answer_bin_id).first()
        else:
            # if they failed it
            # if it's the start and they failed it, just keep the same
            if bin.bin_type == BinTypeEnum.start_bin:
                return False

            next_bin = Bin.query.filter(Bin.id == bin.wrong_answer_bin_id).first()

        # updating the card to be in the right bin and the next_review
        card.update_card(next_bin)
        db.session.commit()
        return True

    # TODO: cleanup of the logic here to be cleaner, overall, of how it's all structured
    # returns a successful bool
    def verify_timestamp(self) -> bool:
        card = Card.query.filter(Card.id == self.card_id).first()
        if card.id != self.card_id:
            return False
        return card.next_review <= datetime.datetime.now()

@dataclass
class NewDeckInput():
    name: str

    def __init__(self, input: dict):
        if ("name" not in input):
            raise Exception("misformed review input")
        self.name = input["name"]
    
    def add_deck(self):
        deck = Deck(name = self.name)
        db.session.add(deck)
        db.session.commit()
