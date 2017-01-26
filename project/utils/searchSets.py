import cardDb

#returns public sets with relevant names
def setSearch(query):
    tupleSets = getAllSets()
    ret = []
    for set in tupleSets:
        if (set[2].lower()).find(query.lower()) >= 0:
            ret.insert(set)
    return ret
