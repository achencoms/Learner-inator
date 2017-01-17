from flask import Flask, render_template, request, session, url_for, redirect
import hashlib

app = Flask(__name__)
app.secret_key = "secrets"

#Site Navigation
@app.route("/")
def root():
    if isLoggedIn():
        return render_template('home.html')
    else:
        return render_template('home.html')

@app.route("/login", methods = ["POST"])
def login():
    #request
    username = request.form["username"]
    password = request.form["password"]
    #auth
    if isValidAccountInfo(username,password):
        session['userID']=username
        #redirect
    else:
        return render_template('login.html',message='leemao')

@app.route("/register", methods = ["POST"])
def register():
    #request
    username = request.form["username"]
    password = request.form["password"]
    #reg
    if doesUserExist("username"):
        return render_template('login.html',message='leemao1')
    else:
        registerAccountInfo(username,password)
        #do something

#@app.route("/set/<setID>")
#def create(setID):
#    if isLoggedIn():
        
        

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
