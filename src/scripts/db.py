from utils.db import connection_decorator

@connection_decorator
def reset_db(conn):
  cur = conn.cursor()
  cur.execute('DROP SCHEMA IF EXISTS public CASCADE;')
  cur.execute('CREATE SCHEMA public;')
  conn.commit()
  cur.close()
  print('finished making table')
  return 0
