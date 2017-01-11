from flask import Flask, render_template, request, session, url_for, redirect
import 

app = Flask(__name__)
app.secret_key = "secrets"

#Site Navigation
@app.route("/")
def root():
    #if isLoggedIn():
    return render_template('home.html')

@app.route("/set/")
def create():
    #if isLoggedIn():
        

#HELPERS-----------------------------------------------------------------------

#Login Helpers
def isLoggedIn():
    return "userID" in session

def getUserID():
    return session["userID"]

def logout():
    session.pop('userID')

if __name__ == "__main__":
    app.debug = True
    app.run()
