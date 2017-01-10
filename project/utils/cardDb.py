import sqlite3

#PublicSets Table -----------------------------------------------------
#exclusively public templates!

#for ID generation, just use a md5 hash of time and userID/set name


def addSet(setID, creatorID, setName, cardData): #presuming card data is a string for now
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    addSet = "INSERT INTO PublicSets VALUES(%d, %d,'%s','%s');"%(setID, creatorID, setName, cardData)
    c.execute(addSet)
    db.commit()
    db.close()
    
def rmSet(setID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    rmSet = "DELETE FROM PublicSets WHERE setID = '%s';"%(setID)
    c.execute(rmSet)
    db.commit()
    db.close()
    
    
#PrivateCards Table -----------------------------------------------------
def getSets(uID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = d;"%(uID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return None
    return sel[1]
