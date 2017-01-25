import sqlite3
#when private, add to public and private tables

#PublicSets Table -----------------------------------------------------
#exclusively public templates! (what's used for search)

#for ID generation, just use a md5 hash of time and userID/set name

#for viewing public sets...
def getAllSets():
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    nice = "SELECT * FROM PublicSets"
    sel = c.execute(nice)
    ret = sel.fetchall()
    db.close()
    return ret
#should probably be optimized...

def addSet(creatorID, setName, cardData): #presuming card data is a string for now
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    addSet = "INSERT INTO PublicSets (creatorID, setName, cardData) VALUES(%d,'%s','%s');"%(creatorID, setName, cardData)
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

def ownsPublicSet(setID, uID): #can verify from getSets
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    rmSet = "SELECT * FROM PublicSets WHERE setID = '%s' AND uID = %d;"%(setID, uID)
    sel = c.execute(rmSet).fetchone()
    db.close()
    if sel == None:
        return False
    else:
        return True
    
#PrivateCards Table -----------------------------------------------------
def getSets(uID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return None
    return sel[1]

def getSetData(uID, setID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return None
    sets = sel.split("!!")
    for thing in sets:
        a = thing.split("///")
        if a[0] == setID:
            return thing
    return None
    
def ownsSet(setID, uID): #pulled directly from Public table
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
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
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    splitCardData = cardData.split("%%");
    for card in splitCardData: #initialize EF and Interval
        card = card + "EF2.5"
        card = card + "ITCT1"        
        card = card + "ITVL"
        card = card + "CDYR"
        card = card + "CDMN"
        card = card + "CDDT"#no initial values
    adjustedData = "%%".join(splitCardData)
    sets = sel.split("!!")
    newSet = [setID, setName, adjustedData]
    "///".join(newSet)
    sets.append(newSet)
    "!!".join(sets)

def downloadPublicSet(setID, setName, uID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PublicCards WHERE setID = %d;"%(uID)
    sel = c.execute(cmd).fetchone()
    if sel == None:
        return False
    cardData = sel[2]
    setName = sel[0]
    customID = str(setID) + "&" + str(uID)
    splitCardData = cardData.split("%%");
    for card in splitCardData: #initialize EF and Interval
        card = card + "EF2.5"
        card = card + "ITCT1"        
        card = card + "ITVL"
        card = card + "CDYR"
        card = card + "CDMN"
        card = card + "CDDT"#no initial values
    initializedData = "%%".join(splitCardData)
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
    sel = c.execute(cmd).fetchone()
    sets = sel.split("!!")
    newSet = [customID, setName, initializedData]
    "///".join(newSet)
    sets.append(newSet)
    "!!".join(sets)
    db.close()
    
    
def rmFromLibrary(uID, setID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
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

def updateSet(uID, setID, newSetData): #upon close of session, or for editing   
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    sets = sel.split("!!")
    for thing in sets:
        a = thing.split("///")
        if a[0] == setID:
            thing = newSetData
            return
    return False
#if editing, creatorID changes, setID changes 
