from api.models import db

# deck table
class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_on = db.Column(db.DateTime, nullable=False)

# review type table
class ReviewType(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    review_type = db.Column(db.String(50), nullable=False)

# bin table
class Bin(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    from_review_type_id = db.Column(
        db.Integer,
        db.ForeignKey("review_type.id"),
        nullable=False
    )
    to_review_type_id = db.Column(
        db.Integer,
        db.ForeignKey("review_type.id"),
        nullable=False
    )
    time_delay_hours = db.Column(
        db.Integer,
        nullable=False
    )
    incorrect_answer_decrementer = db.Column(
        db.Integer,
        nullable=False
    )

class Card(db.Model):
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
    created_at = db.Column(db.DateTime, nullable=False)
    next_review = db.Column(db.DateTime, nullable=False)

class Vocabulary(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    card_id = db.Column(
        db.Integer,
        db.ForeignKey("card.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
