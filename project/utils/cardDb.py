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

#if creator wants to take public set off public library
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

def ownsSet(setID, uID): #pulled directly from Public table
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = d;"%(uID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    sets = sel.split("!!")
    for thing in sets:
        thing = thing.split("///")
        if thing[0] == setID:
            return False
    return True
    
def addToLibrary(setID, creatorID, setName, cardData, uID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = d;"%(uID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    sets = sel.split("!!")
    newSet = [setID, creatorID, setName, cardData]
    "///".join(newSet)
    sets.append(newSet)
    "!!".join(sets)

def rmFromLibrary(uID, setID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = d;"%(uID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    sets = sel.split("!!")
    for thing in sets:
        a = thing.split("///")
        if a[0] == setID:
            sets.remove(thing)
            return
    return False

    
