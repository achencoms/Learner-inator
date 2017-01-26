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

def getPublicSet(setID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PublicCards WHERE setID = %d;"%(setID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return None
    return sel    
    
    
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
    sets = sel[1].split("!!")
    for thing in sets:
        a = thing.split("///")
        if a[0] == setID:
            return thing
    return ""

def addPrivateSet(setID, uID, setName, setData):
    addSet(uID, setName, setData)
    downloadPublicSet(setID, setName, uID)

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

def downloadPublicSet(setID, setName, uID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PublicSets WHERE setID = %d;"%(setID)
    sel = c.execute(cmd).fetchone()
    print sel
    if sel == None:
        return False
    cardData = sel[3]
    print cardData
    setName = sel[2]
    splitCardData = cardData.split("%%");
    for card in splitCardData: #initialize EF and Interval
        card = card + "||2.5"#EF
        card = card + "||1"#ITCT        
        card = card + "||-1"#ITVL
        card = card + "||9999"#CDYR
        card = card + "||13"#CDMN
        card = card + "||32"#no initial values
    initializedData = "%%".join(splitCardData)
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
    newSet = [str(setID), setName, initializedData]
    newSet = "///".join(newSet)
    sel = c.execute(cmd).fetchone()
    sets = sel[1].split("!!")
    if (len(sets) != 0):
        sets.append(newSet)
        newSet = "!!".join(sets)
    addSet = "UPDATE PrivateCards SET sets = '%s' WHERE uID = %d;"%(newSet, uID)
    c.execute(addSet)
    db.commit()
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
            break
    newSet = "!!".join(sets)
    addSet = "UPDATE PrivateCards SET sets = '%s' WHERE uID = %d;"%(newSet, uID)
    c.execute(addSet)
    db.commit()
    db.close()

#we need to update the database
def updateSet(uID, setID, newSetData): #upon close of session, or for editing   
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
    sel = c.execute(cmd).fetchone()
    if sel[0] == None:
        return False
    sets = sel[1].split("!!")
    print newSetData
    for thing in sets:
        a = thing.split("///")
        print a[0]
        print "This is setID" + setID
        print "This is thing:" + thing
        if a[0] == setID:
            thing = newSetData
            break;	
    newSets = "!!".join(sets)
    print newSets
    addSet = "UPDATE PrivateCards SET sets = '%s' WHERE uID = %d;"%(newSets, uID)
    c.execute(addSet)
    db.commit()
    db.close()
    
#if editing, creatorID changes, setID changes
