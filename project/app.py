from flask import Flask, render_template, request, session, url_for, redirect
import hashlib

app = Flask(__name__)
app.secret_key = "secrets"

# Site Navigation

# NOTE: ALL ROUTES NEED TO END WITH / (ex. /login/ instead of /login)


@app.route("/")
def root():
    if isLoggedIn():
        return render_template('home.html')
    else:
        return render_template('index.html')


@app.route("/login/", methods=["POST"])
def login():
    # request
    username = request.form["username"]
    password = request.form["password"]

    # auth
    return "false"
    # PLEASE MAKE THIS FUNCTION FOR LOGIN TO WORK
    if isValidAccountInfo(username, password):
        session['userID'] = username
        # redirect
        return "true"
    else:
        return "false"


@app.route("/register/", methods=["POST"])
def register():
    # request
    username = request.form["username"]
    password = request.form["password"]

    return "false"
    # reg
    # PLEASE MAKE THESE FUNCTIONS FOR REGISTRATION TO WORK
    if doesUserExist("username"):
        return "false"
    else:
        registerAccountInfo(username, password)
        # do something (aka proceed to sign person in)
        return "true"

# @app.route("/set/<setID>/")
# def create(setID):
#    if isLoggedIn():


# HELPERS-----------------------------------------------------------------------

# Login Helpers
def isLoggedIn():
    return "userID" in session


def getUserID():
    return session["userID"]


def logout():
    session.pop('userID')

if __name__ == "__main__":
    app.debug = True
    app.run()
