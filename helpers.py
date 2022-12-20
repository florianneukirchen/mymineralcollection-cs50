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


# https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def filenamehelper(url, filename):
    if not os.path.exists(os.path.join(url, filename)):
        return filename
    filename = "a" + filename
    return filenamehelper(url, filename)



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

def minlink(value):
    """Add links to mineral names."""
    if not value:
        return ""
    html = '<a href="mineral?n=' + value + '" class="minlink">' + value + '</a>' 
    return html

def addnr(value):
    """Add Nr."""
    if not value:
        return ""
    return '(Nr. ' + value + ')'

def asimg(value):
    """Return img html"""
    if not value:
        return ""
    return '<img src="/uploads/' + value + '">'

def asthumb(value):
    """Return img html"""
    if not value:
        return ""
    return '<img src="/thumb/' + value + '">'

def minithumb(value):
    """Return img html"""
    if not value:
        return ""
    return '<img src="/thumb/' + value + '" width="25px" height="25px">'

def asthumbright(value):
    """Return img html"""
    if not value:
        return ""
    return '<img src="/thumb/' + value + '" class="floatright rounded">'

def shortnotes(value):
    n = 4
    result_list = value.split()
    if len(result_list) < n:
        return value
    return " ".join(result_list[:n]) + "…"

    
    