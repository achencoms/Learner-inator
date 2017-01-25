from flask import Flask, render_template, request, session, url_for, redirect
from utils import userDb
import hashlib

app = Flask(__name__)
app.secret_key = "secrets"

# Site Navigation

# NOTE: ALL ROUTES NEED TO END WITH / (ex. /login/ instead of /login)


@app.route("/")
def root():
    return render_template('index.html')
    # Turn this back on once /home/ is working
    """
    if isLoggedIn():
        return render_template('home.html')
    else:
        return render_template('index.html')
    """


@app.route("/login/", methods=["POST"])
def login():
    # request
    username = request.form["username"]
    password = request.form["password"]
    #auth
    if userDb.isValidAccountInfo(username,password):
        session['userID'] = userDb.getUserID(username)
        return "true"
    else:
        return "false"


@app.route("/register/", methods=["POST"])
def register():
    # request
    username = request.form["username"]
    password = request.form["password"]
    #reg
    if userDb.doesUserExist("username"):
        return "false"
    else:
        userDb.registerAccountInfo(username,password)
        session['userID'] = userDb.getUserID(username)
        return "true"

@app.route("/createSet/")
def create():
    if isLoggedIn():
        


@app.route("/set/<setID>/")
def set(setID):
    if isLoggedIn():
        cardDb.addSet()


# HELPERS-----------------------------------------------------------------------

# Login Helpers
def isLoggedIn():
    return "userID" in session


def getUserID():
    return session["userID"]


def logout():
    session.pop('userID')

def hash(unhashed):
    return hashlib.md5(unhashed).hexdigest()

if __name__ == "__main__":
    app.debug = True
    app.run()
