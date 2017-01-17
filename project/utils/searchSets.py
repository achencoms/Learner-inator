import cardDb

#returns public sets with relevant names
def setSearch(query):
    tupleSets = getAllSets()
    ret = []
    for set in tupleSets:
        if set[2].lower() == setName.lower():
            ret.insert(set)
    return ret
