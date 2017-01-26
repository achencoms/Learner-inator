import sqlite3
#when private, add to public and private tables

#PublicSets Table -----------------------------------------------------
#exclusively public templates! (what's used for search)

#for ID generation, just use a md5 hash of time and userID/set name

#for viewing public sets...
def getAllSets():
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    nice = "SELECT * FROM PublicSets;"
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
    toggleVis(creatorID, getPublicSetID(creatorID, setName), 1)

def getPublicSetID(creatorID, setName):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    nice = "SELECT * FROM PublicSets WHERE creatorID = %d AND setName = %d;"%(creatorID, setName)
    sel = c.execute(nice).fetchone()
    db.close()
    if sel == None:
        return False
    return sel[0]

#if creator wants to take public set off public library, force toggles vis
def rmSet(setID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    rmSet = "DELETE FROM PublicSets WHERE setID = '%s';"%(setID)
    c.execute(rmSet)
    db.commit()
    db.close()
    privatize(setID)

def getPublicSetName(setID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    nice = "SELECT * FROM PublicSets WHERE setID = %d;"%(setID)
    sel = c.execute(nice).fetchone()
    db.close()
    if sel == None:
        return False
    return sel[2]

    
def ownsPublicSet(setID, uID): #can verify from getSets
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    rmSet = "SELECT * FROM PublicSets WHERE setID = '%s' AND creatorID = %d;"%(setID, uID)
    sel = c.execute(rmSet).fetchone()
    db.close()
    if sel == None:
        return False
    else:
        return True

def addToPublicSet(setID, uID, cardData):#owner editing (will morph id) #NOT DONE
    if ownsPublicSet(setID, uID):
        db = sqlite3.connect("data/main.db")
        c = db.cursor()
        rmSet = "SELECT * FROM PublicSets WHERE setID = '%s' AND creatorID = %d;"%(setID, uID)
        sel = c.execute(rmSet).fetchone()
        if sel == None:
            return False
        else:
            sets = sel[3].split("%%")
            sets.append(cardData)
            newSets = "%%".join(sets)
            addSet = "UPDATE PublicSets SET cardData = '%s' WHERE setID = '%s';"%(newSets, setID)
            c.execute(addSet)
            db.commit()
            db.close()
    else:
        return False

        
def getPublicSet(setID):
    if (!isPublic(setID)):
        return None
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PublicSets WHERE setID = %d;"%(setID)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return None
    return sel    

def getPublicSetData(setID):
    return getPublicSet[2]
    
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
    print "this is sel"
    print sel
    sets = sel[1].split("!!")
    for thing in sets:
        a = thing.split("///")
        print "this is a thing"
        print thing
        print a
        if a[0] == str(setID):
            return thing
    return ""

def addPrivateSet(uID, setName, setData, vis):
    addSet(uID, setName, setData)
    setID = getPublicSetID(uID, setName)
    downloadPublicSet(setID, setName, uID)
    toggleVis(uID, setID, vis)

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
    addVis(uID, setID, vis)
    
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
    rmVis(uID, setID)

#we need to update the database
def updateSet(uID, setID, newSetData): #upon close of session, or for editing   
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM PrivateCards WHERE uID = %d;"%(uID)
    sel = c.execute(cmd).fetchone()
    if sel == None:
        return False
    sets = sel[1].split("!!")
    print newSetData
    marker = 0
    for x in range(0, len(sets)):
        a = sets[x].split("///")
        if a[0] == setID:
            marker = x
            break;	
        sets[marker] = newSetData
    newSets = "!!".join(sets)
    addSet = "UPDATE PrivateCards SET sets = '%s' WHERE uID = %d;"%(newSets, uID)
    c.execute(addSet)
    db.commit()
    db.close()
    
#if editing, creatorID changes, setID changes
def editSet(uID, setID, newSetData):
    #take old vis off the market
    rmVis(uID, setID)    
    addPrivateSet(uID, getPublicSetName(setID), newSetData, 0)
    
#Visibility table 1 for visible means public
#------------------------------------
def toggleVis(uID, setID, goal):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    tog = "UPDATE VISIBILITY SET vs = %d WHERE uID = %d AND setID = %d;"%(goal, uID, setID)
    c.execute(tog)
    db.commit()
    db.close()

def addVis(uID, setID, vis):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    addem = "INSERT INTO VISIBILITY (UID, setID, vis) VALUES(%d, %d, %d);"%(uID, setID, vis)
    c.execute(addem)
    db.commit()
    db.close()

def removeVis(uID, setID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    dele = "DELETE FROM VISIBILITY WHERE uID = %d AND setID = %d;"%(uID, setID)
    c.execute(dele)
    db.commit()
    db.close()

def getVis(uID, steID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    getem = "SELECT * FROM VISIBILITY WHERE uID = %d AND setID = %d;"%(uID, setID)
    ret = c.execute(getem).fetchone()
    db.close()
    if ret == None:
        return False
    else:
        return ret

def isPublic(setID):#set is public if someone has it as public
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    getem = "SELECT * FROM VISIBILITY WHERE setID = %d;"%(setID)
    ret = False
    for row in c.execute(getem):
        if row[2] == 1: #someone has it as public
            ret = True
    db.close()
    return ret

def privatize(setID): #force toggle everyones
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    getem = "SELECT * FROM VISIBILITY WHERE setID = %d;"%(setID)
    ret = False
    for row in c.execute(getem):
        row[2] == 0
    db.close()
    return ret
