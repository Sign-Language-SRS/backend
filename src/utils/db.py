import os
import psycopg2
import datetime

# a decorator function that passes in the connection
def connection_decorator(func):
	def wrapper_func():
		conn = psycopg2.connect(
				database=os.environ['POSTGRES_DB'],
				user=os.environ['POSTGRES_USER'],
				password=os.environ['POSTGRES_PASSWORD'],
				host=os.environ['POSTGRES_HOSTNAME'],
				port=os.environ['POSTGRES_PORT']
    	)
		output = func(conn)
		conn.close()
		return output
	return wrapper_func

# a decorator function that passes in the connection
def sqlalchemy_connection_decorator(func):
	def wrapper_func():
		from sqlalchemy import create_engine
		engine = create_engine(( 
      "postgresql://"
      f"{os.environ['POSTGRES_USER']}:"
      f"{os.environ['POSTGRES_PASSWORD']}@"
      f"{os.environ['POSTGRES_HOSTNAME']}:"
      f"{os.environ['POSTGRES_PORT']}/"
      f"{os.environ['POSTGRES_DB']}"
		), echo=True)
		
		return func(engine)
	return wrapper_func

def round_to_next_hour(t):
	return t.replace(second=0, microsecond=0, minute=0, hour=t.hour)

def context_sensitive_rounded_up_time():
  return round_to_next_hour(datetime.datetime.now())
