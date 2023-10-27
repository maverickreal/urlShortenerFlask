import sqlite3
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for


def get_db_conn():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
hashids = Hashids(min_length=6, salt=app.config["SECRET_KEY"])


@app.route("/", methods=["GET"])
def index():
    return render_template("./index.html")


@app.route("/", methods=["POST"])
def shorten_url():
    url = request.form["url"]
    print("here", url)
    if not url:
        flash("Please enter a valid URL", "error")
        return redirect(url_for("index"))
    conn = get_db_conn()
    url_data = conn.execute("INSERT INTO urls(original_url) VALUES(?)", (url,))
    conn.commit()
    conn.close()
    url_id = url_data.lastrowid
    hashid = hashids.encode(url_id)
    Short_Url = request.host_url + hashid
    return render_template("./index.html", short_url=Short_Url)
