import json
import io
import os

from numpy import size
from Error import ERRCODE, Error
from EngineConstants import checkEngineConstant, isFieldValid
import Common
from EngineConstants import getEngineConstants
import networkx as nx
import matplotlib.pyplot as plt

def checkConnectingNodes(roomsList, filePath, keyNames):
    fails = list()
    for room in roomsList:
        for n in room['NodeConnections']:
            name = room['NodeConnections'][n]['ConnectingNode']

            if(keyNames.containsNode(name) != True):
                fails.append(Error(ERRCODE.NODE_DOES_NOT_EXISTS, filePath,
                          f"{name} node does not exists"))

    return len(fails) > 0, fails

def checkTransitable(roomsList, filePath, showMap):
    fails = list()
    mapGraph = nx.DiGraph()

    for room in roomsList:
        for n in room['NodeConnections']:
            other = room['NodeConnections'][n]['ConnectingNode']
            mapGraph.add_edge(room['Name'],other)            

    if not nx.is_strongly_connected(mapGraph) :
        fails.append(Error(ERRCODE.MAP_NODE_NOT_ACCESIBLE, filePath,
                          f"Some node/s is/are not accesible from other nodes"))
        strongComp = nx.strongly_connected_components(mapGraph)
    
    if not nx.is_weakly_connected(mapGraph):
        fails.append(Error(ERRCODE.MAP_IS_NOT_CONECTED, filePath,
                          f"Some node/s is/are not conected to the other nodes"))

    #Cosas de pintar
    pos = nx.planar_layout(mapGraph)
    nx.draw_networkx_edges(mapGraph, pos=pos, alpha= 0.5, node_size=500)
    nx.draw_networkx_labels(mapGraph, pos=pos, alpha= 1,clip_on=False)
    if showMap: plt.show()
    plt.savefig("map.png")

    return fails

def checkEnemyEvent(event, filePath, errorList, keyNames):
    if('Enemy' in event):
        if(keyNames.containsEnemy(event['Enemy']) != True):
            errorList.append(Error(ERRCODE.MAP_ENEMY_DOES_NOT_EXIST, filePath,
                f"{event['Enemy']} enemy does not exist"))
    elif('Enemies' in event):
        for enemy in event['Enemies']:
            if(keyNames.containsEnemy(enemy) != True):
                errorList.append(Error(ERRCODE.MAP_ENEMY_DOES_NOT_EXIST, filePath,
                    f"{enemy} enemy does not exist"))
    else:
        errorList.append(Error(ERRCODE.EVENT_MISSING_FIELD, filePath,
            f"{event} node does not have enemy/enemies"))
    return

def checkSingleEvent(event, filePath, folderPath, errorList, keyNames):
    requiredFields = getEngineConstants(event['EventType'])
    for field in requiredFields:
        if(field not in event):
            errorList.append(Error(ERRCODE.EVENT_MISSING_FIELD, filePath,
                        f"{field} does not exist in event"))
        elif(field == 'ItemLots'):
            if(keyNames.containsItem(event['ItemLots'][0]['Item']) != True):
                errorList.append(Error(ERRCODE.MAP_ITEM_DOES_NOT_EXIST, filePath,
                    f"{event['ItemLots'][0]['Item']} item does not exist"))
    if(event['EventType'] == 'eStartBattle'):
        checkEnemyEvent(event, filePath, errorList, keyNames)
    if(event['EventType'] == 'eSendAudio'):
        if(checkAudio(event['AudioName'], folderPath) == False) : 
            errorList.append(Error(ERRCODE.MAP_AUDIO_DOES_NOT_EXIST, filePath,
                    f"{event['AudioName']} audio does not exist"))
    if(event['EventType'] == 'eSendImage'):
        if(checkImage(event['ImageName'], folderPath) == False) : 
            errorList.append(Error(ERRCODE.MAP_IMAGE_DOES_NOT_EXIST, filePath,
                    f"{event['ImageName']} image does not exist"))

def checkEventType(event, filePath, folderPath, errorList, keyNames):
    for e in event:
        if(checkEngineConstant(e['EventType'], "EVENTTYPE") != True):
            errorList.append(Error(ERRCODE.NODE_EVENT_DOES_NOT_EXIST, filePath,
                        f"{e['EventType']} event does not exist"))
        else:
            checkSingleEvent(e, filePath, folderPath, errorList, keyNames)

def checkEvents(roomsList, filePath, folderPath, keyNames):
    fails = list()
    events = getEngineConstants("EVENTS")
    
    for room in roomsList:
        for event in events:			 
            if(event in room):
                checkEventType(room[event], filePath, folderPath, fails, keyNames)
    return len(fails) > 0, fails

def checkMapKeys(roomsList, filePath):
    fails = list()

    # Contains objects with the required keys
    completedRoomsList = []

    for idx, room in enumerate(roomsList):
        validRoom = True
        res, errors = Common.ExistKeys(filePath, ["NodeConnections"], [], room, idx)
        if res:
            validRoom = False
            for err in errors:
                fails.append(err)
        else:
            nodeConnections = room['NodeConnections']
            for connection in nodeConnections:
                res, errors = Common.ExistKeys(filePath, ["ConnectingNode"], [], nodeConnections[connection], idx)
                if res:
                    validRoom = False
                    for err in errors:
                        fails.append(err)

        res, errors = Common.ExistKeysOnEvents(filePath, ["OnArriveEvent","OnExitEvent","OnInspectEvent"], room, idx)
        if res:
            validRoom = False
            for err in errors:
                fails.append(err)
        
        if validRoom: completedRoomsList.append(room)
                    
    return len(fails) > 0, fails, completedRoomsList

def checkInvalidFields(roomsList):
    invalidFields = dict()
    for room in roomsList:
        inv = [i for i in room.keys() if not isFieldValid(i, "Maps")]
        if len(inv) > 0:
            invalidFields[room["Name"]] = inv
    return len(invalidFields) > 0, invalidFields

# The given image file must exist in the filePath
def checkImage(image, folderPath):
    imagesPath = folderPath + '/images/' + image
    if (os.path.isfile(imagesPath) != True):
        return False
    return True

# The given audio file must exist in the filePath
def checkAudio(audio, folderPath):
    audiosPath = folderPath + '/audios/' + audio
    if (os.path.isfile(audiosPath) != True):
        return False
    return True

def checkAll(filesFolder, keyNames,showMap):
    print(f"\nChecking Map and Nodes...")
    errorList = list()
    filePath = filesFolder + '/map.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        roomsList = json.loads(json_data.read())

    # Exist keys
    res, fails, newList = checkMapKeys(roomsList, filePath)
    if res: roomsList = newList
    for err in fails:
        errorList.append(err)
    print(f"Map missing keys errors: {len(fails)}")

    # Repeat keys
    repeatKeysLen = 0
    for node in roomsList:
        # TODO return for html
        res, fails = Common.RepeatKeys(filePath, node)
        if res:
            for err in fails:
                errorList.append(err)
            repeatKeysLen += len(fails)
    print(f"Map repeat keys errors: {repeatKeysLen}")

    #Map errors
    res, fails = checkConnectingNodes(roomsList, filePath, keyNames)
    for err in fails:
        errorList.append(err)
    print(f"Map connecting nodes errors: {len(fails)}")

    res, fails = checkEvents(roomsList, filePath, filesFolder, keyNames)
    for err in fails:
        errorList.append(err)
    print(f"Map events errors: {len(fails)}")
    
    fails= checkTransitable(roomsList, filePath, showMap)
    for err in fails:
        errorList.append(err)
    print(f"Map connectivity errors: {len(fails)}")

    # Nodes with extra keys
    res, eMessages = checkInvalidFields(roomsList)
    for k, v in eMessages.items():
        errorList.append(Error(ERRCODE.COMMON_INVALID_FIELD,
                        filePath, f'"{k}" has invalid fields {v}'))
        print(f'"{k}" has invalid fields {v}')
    print(f"Nodes with invalid fields: {len(eMessages)}")

    return errorList
