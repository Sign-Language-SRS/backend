from utils.db import connection_decorator

@connection_decorator
def init_db(conn):
  cur = conn.cursor()
  cur.execute('DROP TABLE IF EXISTS books;')
  cur.execute('CREATE TABLE books (id serial PRIMARY KEY);')
  conn.commit()
  cur.close()
  print('finished making table')
  return 0
