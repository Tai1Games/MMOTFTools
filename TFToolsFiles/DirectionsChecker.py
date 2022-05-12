import io, json
import Common
from Error import Error,ERRCODE

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

def testRepeatedDirection(directions):
    dirNames = [item[0] for item in directions]
    duplicates = [dir for dir in dirNames if dirNames.count(dir) > 1]
    unique_duplicates = list(set(duplicates))

    return len(duplicates) > 0, unique_duplicates



def synonymsMatrix(directionsData):
    matrix = list()

    for i in directionsData:
        synonyms = i["Synonyms"]
        synonyms.insert(0, i["Direction"])
        matrix.append(synonyms)

    return matrix

def checkAll(folder):
    errorList = list()
    #TODO loop throug all files named directionSynonyms_*.json
    filePath = folder+'/directionSynonyms.json'

    with io.open(filePath, encoding='utf-8-sig') as json_data:
        directionsList = json.loads(json_data.read())

    # Exist keys
    ExistKeysList = []
    # Contains objects with the required keys
    completedDirectionsList = []
    for dir in directionsList:
        # TODO return for html
        res, fails = Common.ExistKeys(filePath, ["Direction", "Synonyms"], [], dir)
        if res > 0:
            ExistKeysList.append(fails)
        else:
            completedDirectionsList.append(dir)
    directionsList = completedDirectionsList
    print(f"Direction missing keys check errors: {len(ExistKeysList)}")

    matrix = synonymsMatrix(directionsList)
    #Repeated direction
    res, repeats = testRepeatedDirection(matrix)
    for error in repeats:
        errorList.append((ERRCODE.DIR_REPEATED_DIRECTION, filePath,
                          f"{error} direction is duplicate"))
    #Repeated alias
    res, repeats = testSynonyms(matrix)
    for k, v in repeats.items():
        errorList.append((Error.ERRCODE.DIR_REPEATED_SYNONYM, filePath,
                          f"{k} repeated in {v}"))
    for err in errorList:
        print(err)

