from api.app import create_app
from utils.db import sqlalchemy_connection_decorator
from sqlalchemy.orm import Session


@sqlalchemy_connection_decorator
def populate_prototypes(engine):
  with Session(engine) as session:
    # database stuff - should be initialized with create_app
    from api.models.reviews import Deck, Card, Bin, ReviewType, BinTypeEnum, Vocabulary

    # create the japanese deck
    deck = Deck(
      name = "日本語"
    )

    session.add(deck)
    session.commit()

    # create the review types
    # three of them: 1. japanese to english, 2. english to japanese and 3. sentence to english
    japanese = ReviewType(review_type = "japanese")
    english = ReviewType(review_type = "english")
    sentence = ReviewType(review_type = "sentence")
    english_sentence = ReviewType(review_type = "english_sentence")

    session.add(japanese)
    session.add(english)
    session.add(sentence)
    session.add(english_sentence)
    session.commit()

    # create the bins for review
    # this is the first bin, so doesn't matter...
    japanese_to_english_one = Bin(
      from_review_type_id = japanese.id,
      to_review_type_id = english.id,
      time_delay_hours = 0,
      bin_type = BinTypeEnum.start_bin,
      id = 1
    )
    session.add(japanese_to_english_one)
    session.commit()

    english_to_japanese_one = Bin(
      from_review_type_id = english.id,
      to_review_type_id = japanese.id,
      time_delay_hours = 1,
      wrong_answer_bin_id = japanese_to_english_one.id,
      bin_type = BinTypeEnum.middle_bin,
      id = 2
    )
    session.add(english_to_japanese_one)
    session.commit()

    sentence_to_english_one = Bin(
      from_review_type_id = sentence.id,
      to_review_type_id = english_sentence.id,
      time_delay_hours = 2,
      wrong_answer_bin_id = english_to_japanese_one.id,
      bin_type = BinTypeEnum.middle_bin,
      id = 3
    )
    session.add(sentence_to_english_one)
    session.commit()

    japanese_to_english_two = Bin(
      from_review_type_id = japanese.id,
      to_review_type_id = english.id,
      time_delay_hours = 0,
      wrong_answer_bin_id = sentence_to_english_one.id,
      bin_type = BinTypeEnum.middle_bin,
      id = 4
    )
    session.add(japanese_to_english_two)
    session.commit()

    english_to_japanese_two = Bin(
      from_review_type_id = english.id,
      to_review_type_id = japanese.id,
      time_delay_hours = 1,
      wrong_answer_bin_id = japanese_to_english_two.id,
      bin_type = BinTypeEnum.middle_bin,
      id = 5
    )
    session.add(english_to_japanese_two)
    session.commit()

    sentence_to_english_two = Bin(
      from_review_type_id = sentence.id,
      to_review_type_id = english_sentence.id,
      time_delay_hours = 2,
      wrong_answer_bin_id = english_to_japanese_two.id,
      bin_type = BinTypeEnum.end_bin,
      id = 6
    )
    session.add(sentence_to_english_two)
    session.commit()

    # then we need to link it forward, i.e. add in what the next bin is
    def update_bin(start_bin: Bin, next_bin: Bin):
      session.query(Bin)\
        .filter(Bin.id == start_bin.id)\
        .update({Bin.correct_answer_bin_id: next_bin.id}, synchronize_session=False)

    update_bin(japanese_to_english_one, english_to_japanese_one)
    update_bin(english_to_japanese_one, sentence_to_english_one)
    update_bin(sentence_to_english_one, japanese_to_english_two)

    update_bin(japanese_to_english_two, english_to_japanese_two)
    update_bin(english_to_japanese_two, sentence_to_english_two)
    session.commit()

    # adding in cards now
    japanese_vocab = process_csv()

    # for each of the vocabs, we add in a new card
    for vocab in japanese_vocab:
      card = Card(
        bin_id = japanese_to_english_one.id,
        deck_id = deck.id
      )
      session.add(card)
      session.commit()

      # generate four vocabs
      japanese_word = Vocabulary(
        card_id = card.id,
        vocab = vocab[0],
        review_type_id = japanese.id
      )

      english_word = Vocabulary(
        card_id = card.id,
        vocab = vocab[1],
        review_type_id = english.id
      )

      japanese_sentence = Vocabulary(
        card_id = card.id,
        vocab = vocab[2],
        review_type_id = sentence.id
      )

      english_phrase = Vocabulary(
        card_id = card.id,
        vocab = vocab[3],
        review_type_id = english_sentence.id
      )

      session.add(japanese_word)
      session.add(english_word)
      session.add(japanese_sentence)
      session.add(english_phrase)
      session.commit()

def process_csv():
  # add cards next
  import csv

  vocab = []

  with open("/src/scripts/japanese_reviews.csv", newline='') as japanese_file:
    file_reader = csv.reader(japanese_file, delimiter=',', quotechar='|')
    for row in file_reader:
      vocab.append(row)
      print(row)
    return vocab
