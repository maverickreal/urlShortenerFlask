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


@app.route("/", methods=("GET",))
def index():
    return render_template("./index.html")


@app.route("/", methods=("POST",))
def shorten_url():
    url = request.form["url"]
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


@app.route("/<short_url>", methods=("GET",))
def get_original_link(short_url):
    conn = get_db_conn()
    original_id = hashids.decode(short_url)
    if not original_id:
        flash("Invalid URL", "error")
        return redirect(url_for("index"))
    original_id = original_id[0]
    url_data = conn.execute(
        "SELECT original_url, clicks FROM urls WHERE id=(?)", (original_id,)
    ).fetchone()
    if not url_data:
        flash("Invalid URL", "error")
        return redirect(url_for("index"))
    short_url = url_data["original_url"]
    clicks = url_data["clicks"]
    conn.execute("UPDATE urls SET clicks=? where id=?", (clicks + 1, original_id))
    conn.commit()
    conn.close()
    return redirect(short_url)


@app.route("/<short_url>/stats", methods=("GET",))
def get_url_stats(short_url):
    conn = get_db_conn()
    original_id = hashids.decode(short_url)
    if not original_id:
        flash("Invalid URL", "error")
        return redirect(url_for("index"))
    original_id = original_id[0]
    url_data = conn.execute(
        "SELECT original_url, clicks, created FROM urls WHERE id=(?)", (original_id,)
    ).fetchone()
    if not url_data:
        flash("Invalid URL", "error")
        return redirect(url_for("index"))
    Clicks = url_data["clicks"]
    Original_url = url_data["original_url"]
    Created = url_data["created"]
    conn.close()
    return render_template(
        "stats.html", clicks=Clicks, created=Created, original_url=Original_url
    )
