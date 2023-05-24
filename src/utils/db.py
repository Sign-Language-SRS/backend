import os
import psycopg2

# a decorator function that passes in the connection
def connection_decorator(func):
	def wrapper_func():
		conn = psycopg2.connect(
				database=os.environ['POSTGRES_DB'],
				user=os.environ['POSTGRES_USER'],
				password=os.environ['POSTGRES_PASSWORD'],
				host=os.environ['POSTGRES_HOSTNAME'],
				port = '5432'
    	)
		output = func(conn)
		conn.close()
		return output
	return wrapper_func
