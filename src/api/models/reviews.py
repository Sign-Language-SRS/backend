from api.models import db
from dataclasses import dataclass
from typing import List, Optional
import datetime, json

# enum imports
from enum import IntEnum

# helper functions
from utils.db import context_sensitive_rounded_up_time

# deck table
@dataclass
class Deck(db.Model):
    id: int
    name: str
    created_on: datetime

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

# review type table
@dataclass
class ReviewType(db.Model):
    id: int
    review_type: str

    id = db.Column(db.Integer, primary_key=True, unique=True)
    review_type = db.Column(db.String(50), nullable=False)

# enum type to hold the type of bin we want
class BinTypeEnum(IntEnum):
    start_bin = 1
    middle_bin = 2
    end_bin = 3

# bin table
@dataclass
class Bin(db.Model):
    id: int
    from_review_type_id: db.mapped_column(db.ForeignKey("review_type.id"))
    to_review_type_id: db.mapped_column(db.ForeignKey("review_type.id"))
    time_delay_hours: int
    wrong_answer_bin_id: int
    correct_answer_bin_id: int
    bin_type: BinTypeEnum

    id = db.Column(db.Integer, primary_key=True, unique=True)
    from_review_type_id = db.Column(
        db.Integer,
        db.ForeignKey("review_type.id"),
        nullable=True
    )
    to_review_type_id = db.Column(
        db.Integer,
        db.ForeignKey("review_type.id"),
        nullable=True
    )
    time_delay_hours = db.Column(
        db.Integer,
        nullable=True
    )
    wrong_answer_bin_id = db.Column(
        db.Integer,
        db.ForeignKey("bin.id"),
        nullable=True
    )
    correct_answer_bin_id = db.Column(
        db.Integer,
        db.ForeignKey("bin.id"),
        nullable=True
    )
    bin_type = db.Column(
        db.Integer
    )

    from_review_type = db.relationship("ReviewType", foreign_keys=from_review_type_id)
    to_review_type = db.relationship("ReviewType", foreign_keys=to_review_type_id)

@dataclass
class Card(db.Model):
    id: int
    bin_id: db.mapped_column(db.ForeignKey("bin.id"))
    deck_id: int
    created_at: datetime
    next_review: datetime
    vocabs: db.Mapped[List["Vocabulary"]] = db.relationship()
    bin: db.Mapped["Bin"] = db.relationship()

    id = db.Column(db.Integer, primary_key=True, unique=True)
    bin_id = db.Column(
        db.Integer,
        db.ForeignKey("bin.id"),
        nullable=False
    )
    deck_id = db.Column(
        db.Integer,
        db.ForeignKey("deck.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    next_review = db.Column(
        db.DateTime,
        nullable=False,
        default=context_sensitive_rounded_up_time
    )

    def get_bin(self) -> Bin:
        return Bin.query.filter(Bin.id == self.bin_id).first()
    def update_card(self, bin: Bin):
        self.bin_id = bin.id
        self.next_review = datetime.datetime.now()\
            + datetime.timedelta(minutes=bin.time_delay_hours)

@dataclass
class Vocabulary(db.Model):
    id: int
    card_id: db.Mapped[int] = db.mapped_column(db.ForeignKey("card.id"))
    vocab: str
    review_type_id: int

    id = db.Column(db.Integer, primary_key=True, unique=True)
    card_id = db.Column(
        db.Integer,
        db.ForeignKey("card.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    vocab = db.Column(db.String(256), nullable=False)
    review_type_id = db.Column(
        db.Integer,
        db.ForeignKey("review_type.id", onupdate="CASCADE", ondelete="CASCADE")
    )

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
        return card.next_review < datetime.datetime.now()
