import io, json
import Error

#returns a list of lists with format (repeated synonym, ... name of directions that use it ...
def testSynonyms(directions):
    repeats = list()

    for i, dir in enumerate(directions):
        for dirAlias in dir:
            foundIn = list()
            #Check against all other directions
            for otherDirs in filter(lambda x: x != dir, directions):
                if dirAlias in otherDirs:
                    foundIn.append(otherDirs[0])
            if len(foundIn) > 0:
                foundIn.insert(0, dir[0])
                foundIn.insert(0, dirAlias)
                #Dont add duplicate values
                if len(repeats) == 0 or not any(element[0] == dirAlias for element in repeats):
                    repeats.append(foundIn)
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
    for error in repeats:
        errorList.append((Error.ERRCODE.DIR_REPEATED_SYNONYM, filePath,
                          ("{1} repeated in {0}".format(error[0], error[1:]))))
    #print(errorList)

