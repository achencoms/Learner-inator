from flask import Flask, render_template, request, session, url_for, redirect
from utils import userDb, cardDb
import hashlib

app = Flask(__name__)
app.secret_key = "secrets"

# Site Navigation

# NOTE: ALL ROUTES NEED TO END WITH / (ex. /login/ instead of /login)


@app.route("/")
def root():
    #print cardDb.downloadPublicSet(1, "batter", 30)
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

#@app.route("/createSet/")
#def create():
#    if isLoggedIn():
'''     


@app.route("/set/<setID>/")
def set(setID):
    if isLoggedIn():
        cardDb.addSet()
'''

@app.route("/pullData/<setID>/")
def pullData(setID):
    if isLoggedIn():
        tuple = cardDb.getSetData(session['userID'],setID)
        #tuple : (setName, setID, <setData>)
        dict = {}
        dict["setName"] = tuple[0]
        dict["setID"] = tuple[1]
        #<setData> = <cardData>%%<cardData>%%<>...
        #<cardData> : <content>||<content>||interCt||interval||cardYr||...
        #<content> : <piece>**<piece>**..

        rawSetData = tuple[2].split("%%")
        parsedSetData = []
        for cardData in rawSetData:
            parsedSetData.append(parseCardData(cardData))
        dict["setData"] = parsedSetData

        #return format : {setName, setID, [<cardData_dict>,...]}
        #<cardData_dict> = {front, back, interCt, interval, cardYr, cardMn, cardDt, cardEF}
        return dict

@app.route("/pushData/<setID>/", methods = ['GET'])
def pushData(setID):
    if isLoggedIn():
        cardData = request.args.get("title") + "||" + request.args.get("description") + "||" + "2.5" + "||" + "1" + "||" + "-1" + "||" + "||" + "9999" + "||" + "13" + "||" + "32"
        newSetData = cardDb.getSetData(session['userID'],setID) + "%%" + cardData
        cardDb.updateSet(session['userID'],setID,newSetData)
        


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

def parseCardData(cardDataString):
    cardDataList = cardDataString.split("||")
    cardDataDict = {"front":cardDataList[0].split("**"),"back":cardDataList[1].split("**"),"interCt":int(cardDataList[2]),"interval":int(cardDataList[3]),"cardYr":int(cardDataList[4]),"cardMn":int(cardDataList[5]),"cardDt":int(cardDataList[6]),"cardEf":float(cardDataList[7])}

if __name__ == "__main__":
    app.debug = True
    app.run()

