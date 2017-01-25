import sqlite3

#AccountInfo Table -----------------------------------------------------
def isValidAccountInfo(uN, hP):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM Users WHERE username = '%s' AND hashedPass = '%s';"%(uN, hP)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    return True

def getUserID(uN):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM Users WHERE username = '%s';"%(uN)
    sel = c.execute(cmd).fetchone()
    db.close()
    return sel[0]

def registerAccountInfo(uN, hP):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()

    cmd = "SELECT uID FROM Users ORDER BY uID DESC;"
    sel = c.execute(cmd).fetchone()
    if sel == None: #non-null
        userID = 1
    else:
        userID = sel[0] + 1
        
    addAT = "INSERT INTO Users VALUES (%d, '%s','%s');"%(userID,uN,hP)
    c.execute(addAT)

    default = ""

    addPT = "INSERT INTO PrivateCards VALUES (%d,'%s');"%(userID, default)

    c.execute(addPT)
    
    
    db.commit()
    db.close()

def doesUserExist(uN):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM Users WHERE username = '%s';"%(uN)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    else:
        return True 

def getPass(userID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM Users WHERE uID = '%s';"%(userID)
    sel = c.execute(cmd).fetchone()
    password = sel[1]
    print password
    db.close()
    return password

def changePass(userID, newPass):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "UPDATE Users SET hashedPass = '%s'WHERE uID = %d;"%(newPass, userID)
    c.execute(cmd)
    db.commit()
    db.close()
    
