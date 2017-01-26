#Initializes database
import sqlite3

db = sqlite3.connect("../data/main.db")
c = db.cursor()

publicSets = "CREATE TABLE PublicSets(setID INTEGER PRIMARY KEY AUTOINCREMENT, creatorID INTEGER, setName TEXT, cardData TEXT);"
c.execute(publicSets)

users = "CREATE TABLE Users(uID INTEGER, username TEXT, hashedPass TEXT);"
c.execute(users)
#discrepancy b/n public/private sets need to be resolved

cards = "CREATE TABLE PrivateCards(uID INTEGER PRIMARY KEY AUTOINCREMENT, sets TEXT);"
c.execute(cards)

visible = "CREATE TABLE VISIBILITY(uID INTEGER, setID INTEGER, vis INTEGER);"
c.execute(visible)

db.commit()
db.close()

#whenever someone makes a set (public or private) add a new id
#whenever someone downloads a set, a new id is made
