import os
import logging

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mineralcollection.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Browse Collection"""
    rows = db.execute("SELECT * FROM specimen WHERE user_id = ?", session["user_id"])
    
  
    return render_template("cards.html", rows=rows)

@app.route("/browse")
@login_required
def browse():
    """Show table of collection"""
    return redirect("/")


@app.route("/table")
@login_required
def table():
    """Show table of collection"""
    
    rows = db.execute("SELECT * FROM specimen WHERE user_id = ?", session["user_id"])
    
  
    return render_template("table.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add Specimen."""

    if request.method == "POST":
        title = request.form.get("title")
        number = request.form.get("number")
        location = request.form.get("location")
        date = request.form.get("date")
        db.execute("INSERT INTO specimen (user_id, my_id, title, location, date, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                       session["user_id"], number, title, location, date, datetime.now())



        return redirect("/table")
    else:
        return render_template("add.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Checks
        if not request.form.get("username"):
            return apology("Enter a username")
        if not request.form.get("password"):
            return apology("Enter a password")
        if not request.form.get("confirmation"):
            return apology("Confirm your password")
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Passwords don't match")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("Username already exists")

        # Store user in sqlite
        # pass id returned by execute to session to log user in
        pwHash = generate_password_hash(request.form.get("password"))
        session["user_id"] = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), pwHash)
        flash('Thanks for registering.')

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/view")
@login_required
def view():
    """View record"""
    id = request.args.get("id")
   
    if not id:
        return apology("File does not exist", 404)
    rows = db.execute("SELECT * FROM specimen WHERE user_id = ? AND id = ?", session["user_id"], id)

    if len(rows) != 1:
        return apology("Invalid specimen ID")
    row = rows[0]
    app.logger.info(row)
      
    return render_template("view.html", row=row)


@app.route("/delete", methods=["POST"])
def deletespecimen():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM specimen WHERE id = ? AND user_id = ?", id, session["user_id"])
    return redirect("/table")