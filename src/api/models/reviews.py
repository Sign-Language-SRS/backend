from api.models import db
from dataclasses import dataclass
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
    from_review_type_id: int
    to_review_type_id: int
    time_delay_hours: int
    incorrect_answer_bin_id: int
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
    incorrect_answer_bin_id = db.Column(
        db.Integer,
        db.ForeignKey("bin.id"),
        nullable=True
    )
    bin_type = db.Column(
        db.Integer
    )

@dataclass
class Card(db.Model):
    id: int
    bin_id: int
    deck_id: int
    created_at: datetime
    next_review: datetime

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

@dataclass
class Vocabulary(db.Model):
    id: int
    card_id: int
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

