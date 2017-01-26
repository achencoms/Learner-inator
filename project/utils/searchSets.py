import cardDb

#returns public sets with relevant names
def setSearch(query):
    tupleSets = getAllSets()
    ret = []
    for aset in tupleSets:
        if (aset[2].lower()).find(query.lower()) >= 0:
            ret.insert(aset)
    return ret
