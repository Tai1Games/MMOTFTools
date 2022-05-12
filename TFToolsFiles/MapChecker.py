import json
import io
from Error import ERRCODE, Error
import Program
import Common

def checkConnectingNodes(roomsList, filePath, errorList, keyNames):
    for room in roomsList:
        for n in room['NodeConnections']:
            name = room['NodeConnections'][n]['ConnectingNode']

            if(keyNames.containsNode(name) != True):
                errorList.append(Error(ERRCODE.NODE_DOES_NOT_EXISTS, filePath,
                          f"{name} node does not exists"))


def checkEnemy(event, filePath, errorList, keyNames):
    if('Enemy' in event):
        if(keyNames.containsEnemy(event['Enemy']) != True):
            errorList.append(Error(ERRCODE.ENEMY_DOES_NOT_EXIST, filePath,
                f"{event['Enemy']} enemy does not exist"))
    elif('Enemies' in event):
        for enemy in event['Enemies']:
            if(keyNames.containsEnemy(enemy) != True):
                errorList.append(Error(ERRCODE.ENEMY_DOES_NOT_EXIST, filePath,
                    f"{enemy} enemy does not exist"))
    else:
        errorList.append(Error(ERRCODE.EVENT_MISSING_FIELD, filePath,
            f"{event} node does not have enemy/enemies"))
    return


def checkSingleEvent(event, filePath, errorList, keyNames):
    requiredFields = Program.getEngineConstants(event['EventType'])
    for field in requiredFields:
        if(field not in event):
            errorList.append(Error(ERRCODE.EVENT_MISSING_FIELD, filePath,
                        f"{field} does not exist in event"))
        elif(field == 'ItemLots'):
            if(keyNames.containsItem(event['ItemLots'][0]['Item']) != True):
                errorList.append(Error(ERRCODE.ITEM_DOES_NOT_EXIST, filePath,
                    f"{event['ItemLots'][0]['Item']} item does not exist"))
    if(event['EventType'] == 'eStartBattle'):
        checkEnemy(event, filePath, errorList, keyNames)

        



def checkEventType(event, filePath, errorList, keyNames):
    for e in event:
        if(Program.checkEngineConstant(e['EventType'], "EVENTTYPE") != True):
            errorList.append(Error(ERRCODE.NODE_EVENT_DOES_NOT_EXIST, filePath,
                        f"{e['EventType']} event does not exist"))
        else:
            checkSingleEvent(e, filePath, errorList, keyNames)



def checkEvents(roomsList, filePath, errorList, keyNames):
    events = Program.getEngineConstants("EVENTS")
    
    for room in roomsList:
        for event in events:			 
            if(event in room):
                checkEventType(room[event], filePath, errorList, keyNames)


def checkAll(filesFolder, keyNames):
    errorList = list()
    filePath = filesFolder + '/mapejemplo.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        roomsList = json.loads(json_data.read())
    
    # Repeat keys
    RepeatKeysList = []
    for node in roomsList:
        # TODO return for html
        res, fails = Common.RepeatKeys("maps.json", node)
        if len(fails) > 0:
            RepeatKeysList.append(fails)
    print(f"{len(RepeatKeysList)} repeat key errors found.")


    #Map errores
    checkConnectingNodes(roomsList, filePath, errorList, keyNames)
    checkEvents(roomsList, filePath, errorList, keyNames)
    
    print(f"{len(errorList)} map errors found.")
    return fails
