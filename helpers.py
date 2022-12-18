import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", code=code, message=message), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def date2(value):
    """Format value as 2 digits."""
    if not value:
        return "__"
    return f"{value:02d}"

def date4(value):
    """Format value as 2 digits."""
    if not value:
        return "____"
    return f"{value:04d}"

def taglink(value):
    """Add links to tags."""
    if not value:
        return ""
    html = '<a href="tag?t=' + value + '">' + value + '</a>' 
    return html

def addnr(value):
    """Add Nr."""
    if not value:
        return ""
    return 'Nr. ' + value