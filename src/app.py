from flask import Flask
from db import connection_decorator

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/init_db")
@connection_decorator
def init_db(conn):
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS books;')
    cur.execute('CREATE TABLE books (id serial PRIMARY KEY);')
    conn.commit()
    cur.close()
    return "succesfully initialized database"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
