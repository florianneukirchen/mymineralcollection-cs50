import os
import logging # usage: app.logger.info(x)

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import re

from helpers import apology, login_required, date2, date4, taglink, addnr

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["date2"] = date2
app.jinja_env.filters["date4"] = date4
app.jinja_env.filters["taglink"] = taglink
app.jinja_env.filters["addnr"] = addnr


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

    # Are we searching?
    q = request.args.get("search")
    if q:
        q = "%" + q + "%"
        

        sql = "SELECT * FROM specimen JOIN specmin ON specmin.specimen_id = specimen.id WHERE user_id = ? AND min_symbol = ?"
        rows = db.execute(sql, session["user_id"], q)

        app.logger.info("query " + q)
        app.logger.info(str(rows))
        return render_template("browse.html", rows=rows)
        
    # Normal behavoir        
    rows = db.execute("SELECT * FROM specimen WHERE user_id = ?", session["user_id"])

    for row in rows:
        row['minerals'] = db.execute("SELECT minerals.name AS name FROM minerals JOIN specmin ON minerals.symbol = specmin.min_symbol WHERE specmin.specimen_id = ?", row['id'])
        row['tags'] = db.execute("SELECT tags.tag AS tag FROM tags JOIN specimen ON tags.specimen_id = specimen.id WHERE specimen.id = ?", row['id'])
   
    return render_template("browse.html", rows=rows)

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

    for row in rows:
        row['minerals'] = db.execute("SELECT minerals.name AS name FROM minerals JOIN specmin ON minerals.symbol = specmin.min_symbol WHERE specmin.specimen_id = ?", row['id'])
        row['tags'] = db.execute("SELECT tags.tag AS tag FROM tags JOIN specimen ON tags.specimen_id = specimen.id WHERE specimen.id = ?", row['id'])
         
    
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
        locality = request.form.get("locality")
        storage = request.form.get("storage")
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")
        tags = request.form.get("tags")
        minerals = request.form.get("minerals")
     
        thumbnail = None

        # CHECK
        if not title:
            return apology("Title is required")
        if day in [str(i) for i in range(1, 32)]:
            day = int(day)
        else:
            day = None
        if month in [str(i) for i in range(1, 13)]:
            month = int(month)
        else:
            month = None
        if len(year) == 4 and year.isdigit():
            year = int(year)
        else:
            year = None

        # Add Specimen to DB
        newid = db.execute("INSERT INTO specimen (user_id, my_id, title, locality, day, month, year, storage, timestamp, thumbnail) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       session["user_id"], number, title, locality, day, month, year, storage, datetime.now(), thumbnail)

        if newid:
            flash('New specimen has been added.')
        else:
            flash('Error, not able to add specimen.')
        
        # Add minerals to DB
        if minerals:
            minerals = minerals.split(',')
            for min in minerals:
                symbol = db.execute("SELECT symbol FROM minerals WHERE name = ?", min)[0]['symbol']
                db.execute("INSERT INTO specmin (specimen_id, min_symbol) VALUES (?,?)", newid, symbol)

        # Add tags to DB
        if tags:
            tags = tags.split(',')
            for tag in tags:
                # Remove dangerous characters
                tag = re.sub('[^a-zA-Z0-9]', '', tag)
                db.execute ("INSERT INTO tags (specimen_id, tag) VALUES (?,?)", newid, tag)
            
        return redirect("/table")
    else:
        # GET
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
def viewspecimen():
    """View record"""
    id = request.args.get("id")
   
    if not id:
        return redirect("/")
    rows = db.execute("SELECT * FROM specimen WHERE user_id = ? AND id = ?", session["user_id"], id)

    if len(rows) != 1:
        return apology("Invalid specimen ID")
    row = rows[0]
    row['minerals'] = db.execute("SELECT minerals.name AS name, minerals.chemistry AS chemistry, minerals.crystal_system AS crystal_system FROM minerals JOIN specmin ON minerals.symbol = specmin.min_symbol WHERE specmin.specimen_id = ?", id)
    row['tags'] = db.execute("SELECT tags.tag AS tag FROM tags JOIN specimen ON tags.specimen_id = specimen.id WHERE specimen.id = ?", row['id'])

    return render_template("view.html", row=row)


@app.route("/delete", methods=["POST"])
def deletespecimen():
    id = request.form.get("id")
    if id:
        rows = db.execute("DELETE FROM specimen WHERE id = ? AND user_id = ?", id, session["user_id"])

        if rows < 1:
            flash('Error, could not delete specimen from database.')
        else:
            flash('Specimen has been deleted from database.')
            
    return redirect("/table")

@app.route("/tag")
def tag():
    """View tags"""
    t = request.args.get("t")
   
    if not t:
        # Show all tags
        rows = db.execute("SELECT DISTINCT tags.tag AS tags FROM tags JOIN specimen ON tags.specimen_id = specimen.id WHERE specimen.user_id = ?", session["user_id"])
        return render_template("tagsall.html", rows=rows)

    rows = db.execute("SELECT * FROM specimen JOIN tags ON tags.specimen_id = specimen.id WHERE specimen.user_id = ? AND tags.tag = ?", session["user_id"], t)      
    
    if len(rows) == 0:
        # Tag did not exist for user, show all tags
        rows = db.execute("SELECT DISTINCT tags.tag AS tags FROM tags JOIN specimen ON tags.specimen_id = specimen.id WHERE specimen.user_id = ?", session["user_id"])
        return render_template("tagsall.html", rows=rows)

    return render_template("browse.html", rows=rows, heading='Tag: '+ t)
    

# JSON API
@app.route("/mineralsearch")
def mineralsearch():
    q = request.args.get("q")
    if q:
        rows = db.execute("SELECT name FROM minerals WHERE name LIKE ? ORDER BY name LIMIT 20",  "%" + q + "%")
    else:
        rows = []
    return jsonify(rows)


