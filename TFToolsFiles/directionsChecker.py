import io, json
import Error

#returns a list of lists with format (repeated synonym, ... name of directions that use it ...
def testSynonyms(directions):
    repeats = dict()

    synonyms = [dir[1:] for dir in directions]
    for synList in synonyms:
        for dirAlias in synList:
            foundIn = list()
            #Check against all other directions
            for otherSyns in filter(lambda x: x != synList, synonyms):
                if dirAlias in otherSyns:
                    foundIn.append(otherSyns[0])
            if len(foundIn) > 0:
                #If the current synonym is a known repeat, append the direction it refers to
                if dirAlias in repeats.keys():
                    repeats[dirAlias].append(directions[synonyms.index(synList)][0])
                else:
                    #Add new duplicate
                    repeats[dirAlias] = [directions[synonyms.index(synList)][0]]
    return len(repeats) > 0, repeats

def synonymsMatrix(path):
    matrix = list()

    with io.open(path, encoding='utf-8-sig') as json_data:
        directionsData = json.loads(json_data.read())

    for i in directionsData:
        synonyms = i["Synonyms"]
        synonyms.insert(0, i["Direction"])
        matrix.append(synonyms)

    return matrix

def checkAll(folder):
    errorList = list()
    #TODO loop throug all files named directionSynonyms_*.json
    filePath = folder+'/directionSynonyms.json'
    matrix = synonymsMatrix(filePath)
    res, repeats = testSynonyms(matrix)
    for k, v in repeats.items():
        errorList.append((Error.ERRCODE.DIR_REPEATED_SYNONYM, filePath,
                          f"{k} repeated in {v}"))
    for err in errorList:
        print(err)

