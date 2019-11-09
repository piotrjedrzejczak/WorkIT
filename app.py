import sqlite3
from flask import Flask, render_template, request, g
app = Flask(__name__)

DATABASE = "database.db"

def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        db = g.database = sqlite3.connect(DATABASE)
    return db

@app.route('/list')

def list():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    con.row_factory = sqlite3.Row

    cur.execute("SELECT * FROM offers limit 2")

    rows = cur.fetchall()
    con.commit()
    con.close()

    return render_template("list.html", rows = rows)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.Close()


if __name__ == '__main__':
   app.run(debug = True)