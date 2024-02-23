import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        if not name:
            redirect("/")

        month = request.form.get("month")
        if not month:
            redirect("/")
        try:
            month = int(month)
        except ValueError:
            redirect("/")
        if month < 0 or month > 12:
            redirect("/")

        day = request.form.get("day")
        if not day:
            redirect("/")
        try:
            day = int(day)
        except ValueError:
            redirect("/")
        if day < 0 or day > 31:
            redirect("/")

        id = request.form.get("id")
        if not id:
            # If person does not exist, create new db entry
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ? )", name, month, day)
        else:
            # If person exists, update db entry
            db.execute("UPDATE birthdays SET name= ?, month= ?, day= ? WHERE id = ?", name, month, day, id)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html

        rows = db.execute("SELECT * FROM birthdays")

        # Sort alphabetically
        sorted_rows = sorted(rows, key=lambda x: x['name'].casefold())

        return render_template("index.html", birthdays=sorted_rows)


@app.route("/delete", methods=["POST"])
def delete():
    # Remove birthday entry from db
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id= ?", id)
    return redirect("/")


@app.route("/edit", methods=["POST"])
def edit():
    # Edit birthday entry from db
    id = request.form.get("id")
    if id:
        res_id = db.execute("SELECT * FROM birthdays WHERE id= ?", id)

        id = res_id[0]['id']
        name = res_id[0]['name']
        month = res_id[0]['month']
        day = res_id[0]['day']

        rows = db.execute("SELECT * FROM birthdays")

        # Sort alphabetically
        sorted_rows = sorted(rows, key=lambda x: x['name'].casefold())

        return render_template("edit.html", id=id, name=name, month=month, day=day, birthdays=sorted_rows)
