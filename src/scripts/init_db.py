from utils.db import connection_decorator

@connection_decorator
def init_db(conn):
  cur = conn.cursor()
  cur.execute('DROP SCHEMA IF EXISTS public CASCADE;')
  cur.execute('CREATE SCHEMA public;')
  conn.commit()

  # defining the deck table:
  cur.execute('''
    CREATE TABLE deck (
    id serial PRIMARY KEY,
    name VARCHAR ( 50 ) UNIQUE NOT NULL,
    created_on TIMESTAMP NOT NULL,
    UNIQUE(id)
    );
  ''')

  # defining the review type table:
  cur.execute('''
    CREATE TABLE review (
      id serial PRIMARY KEY,
      review_type varchar(50),
      UNIQUE(id)
    );
  ''')

  # defining the bin table:
  cur.execute('''
    CREATE TABLE bin (
    id serial PRIMARY KEY,
    from_review_type_id INT NOT NULL,
    to_review_type_id INT NOT NULL,
    time_delay_hours INT NOT NULL,
    incorrect_answer_decrementer INT NOT NULL,
    FOREIGN KEY (from_review_type_id)
      REFERENCES review (id),
    FOREIGN KEY (to_review_type_id)
      REFERENCES review (id),
    UNIQUE(id)
    );
  ''')

  # defining the card table:
  cur.execute('''
    CREATE TABLE card (
    id serial PRIMARY KEY,
    bin_id INT NOT NULL,
    deck_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    next_review TIMESTAMP NOT NULL,
    FOREIGN KEY (deck_id)
      REFERENCES deck (id) ON DELETE CASCADE,
    FOREIGN KEY (bin_id)
      REFERENCES bin (id),
    UNIQUE(id)
    );
  ''')

  # defining the vocabulary table:
  cur.execute('''
    CREATE TABLE vocabulary (
    id serial PRIMARY KEY,
    card_id INT NOT NULL,
    review_type_id INT NOT NULL,
    metadata bytea,
    FOREIGN KEY (card_id)
      REFERENCES card (id) ON DELETE CASCADE,
    FOREIGN KEY (review_type_id)
      REFERENCES review (id),
    UNIQUE(id)
    );
  ''') 
  conn.commit()

  cur.close()
  print('finished making table')
  return 0
