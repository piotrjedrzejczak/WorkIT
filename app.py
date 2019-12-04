import sqlite3
from flask import Flask, render_template, request, g
app = Flask(__name__)

@app.route('/')

def list():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    con.row_factory = sqlite3.Row

    cur.execute("SELECT * FROM offers limit 5")

    rows = cur.fetchall()
    con.commit()
    con.close()

    return render_template("list.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')