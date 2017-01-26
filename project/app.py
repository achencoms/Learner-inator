from flask import Flask, render_template, request, session, url_for, redirect
from utils import userDb, cardDb, searchSets
import hashlib, json

app = Flask(__name__)
app.secret_key = "secrets"

# Site Navigation

# NOTE: ALL ROUTES NEED TO END WITH / (ex. /login/ instead of /login)


@app.route("/")
def root():
    #cardDb.downloadPublicSet(1,"pineapples", 3)
    return render_template('because.html')
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

@app.route("/viewSet/setID")
def viewSet(setID):
    return render_template("viewSet.html")

#@app.route("/createSet/")
#def create():
#    if isLoggedIn():
'''     


@app.route("/set/<setID>/")
def set(setID):
    if isLoggedIn():
        cardDb.addSet()
'''

@app.route("/pullData/<setID>/", methods = ['GET'])
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
        print dict
        return json.dumps(dict)


@app.route("/pullData1/<setID>/")
def pullData1(setID):
    if isLoggedIn():
        tuple = cardDb.getSetData(3,setID)
        #tuple : (setName, setID, <setData>)
        rawSetData = tuple[2].split("%%")
        parsedSetData = {}
        increment = 0
        for cardData in rawSetData:
            parsedSetData[str(increment)]=(parseCardDataFB(cardData))
            increment += 1
        return parsedSetData


@app.route("/pullSet/<setID>/", methods =['GET'])
def pullSet(setID):
    if isLoggedIn():
        tuple = cardDb.getPublicSet(int(setID))
        #tuple : (setID, creatorID, setName, cardData)
        dict = {}
        dict["setName"] = tuple[2]
        dict["setID"] = tuple[0]
        dict["authorName"] = userDb.getUsername(tuple[1])
        dict["authorID"] = tuple[1]
        rawSetData = tuple[3].split("%%")
        parsedSetData = []
        for cardData in rawSetData:
            parsedSetData.append(parseCardData(cardData))
        dict["cards"] = parsedSetData
        return json.dumps(dict)                                          

@app.route("/pullSet1/<setID>/", methods =['GET'])
def pullSet1(setID):
    if isLoggedIn():
        tuple = cardDb.getPublicSet(int(setID))
        #tuple : (setID, creatorID, setName, cardData)
        dict = {}
        dict["setName"] = tuple[2]
        dict["setID"] = tuple[0]
        dict["authorName"] = userDb.getUsername(tuple[1])
        dict["authorID"] = tuple[1]
        rawSetData = tuple[3].split("%%")
        parsedSetData = {}
        increment = 0
        for cardData in rawSetData:
            parsedSetData[str(increment)] = parseCardDataFB(cardData)
            increment += 1
        dict["cards"] = parsedSetData
        print "whose"
        print dict
        return json.dumps(dict)                                     


@app.route("/pushData/<setID>/", methods = ['GET'])
def pushData(setID):
    if isLoggedIn():
        cardData = request.args.get("title") + "||" + request.args.get("desc") #+ "||" + "2.5" + "||" + "1" + "||" + "-1" + "||" + "9999" + "||" + "13" + "||" + "32"
        #newSetData = cardDb.getSetData(3,1) + "%%" + cardData
        #cardDb.updateSet(3,1,newSetData)
        cardDb.addToPublicSet(5,1,cardData)
        #cardDb.updateSet(session['userID'],setID,newSetData)
	return render_template("porque.html") 

@app.route("/createData/", methods = ['GET']) #just creating the set, we don't need to push setData as of now
def createData(setID):
    if isLoggedIn():
        addSet(session["userID"], request.args.get("setName"), "||||||||||||||||")
        return render_template("")
        ##addToLibrary(setID, session["userID"], request.args.get("setName"), "||||||||||||||||", session["userID"])

@app.route("/new/", methods = ["POST"])
def new():
    if isLoggedIn():
        addSet(session["userID"], request.form.get("setName"), (request.form.get("cardList"))["frontText"] + "||" + (request.form.get("cardList"))["imageUrl"] + "**" + (request.form.get("cardList"))["audioUrl"] + "**" + (request.form.get("cardList"))["backText"])
        return render_template("createSet.html")

@app.route("/search/", methods = ["GET"])
def search():
    if isLoggedIn():
        searchTerm = request.args.get("q")
        return render_template("search.html", list = searchSets.setSearch(searchTerm))

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
    cardDataDict = {"front":cardDataList[0].split("**"),"back":cardDataList[1].split("**"),"interCt":int(cardDataList[3]),"interval":int(cardDataList[4]),"cardYr":int(cardDataList[6]),"cardMn":int(cardDataList[7]),"cardDt":int(cardDataList[8]),"cardEf":float(cardDataList[2])}
    return cardDataDict

def parseCardDataFB(cardDataString):
    cardDataList = cardDataString.split("||")
    print cardDataList
    cardDataDict = {"front":cardDataList[0].split("**"),"back":cardDataList[1].split("**")}
    return cardDataDict

if __name__ == "__main__":
    app.debug = True
    app.run()

