import os
from tabnanny import check
import Common, io, json
from Error import ERRCODE, Error
from EngineConstants import checkEngineConstant, isFieldValid

def checkItemsKeys(itemList, filePath):
    fails = list()

    # Contains objects with the required keys
    completedItemsList = []

    for idx, item in enumerate(itemList):
        validItem = True
        try:
            if item["ItemType"] == "EquipableItem":
                res, errors = Common.ExistKeys(filePath, ["GearSlot"], [], item, idx)
                if res:
                    validItem = False
                    for err in errors:
                        fails.append(err)
        except KeyError:
                res, errors = Common.ExistKeys(filePath, ["Key_Words"], [], item, idx)
                if res:
                    validItem = False
                    for err in errors:
                        fails.append(err)

        res, errors = Common.ExistKeysOnEvents(filePath, ["OnEquipEvents","OnUnequipEvents"], item, idx)
        if res:
            validItem = False
            for err in errors:
                fails.append(err)

        if validItem: completedItemsList.append(item)

    return len(fails) > 0, fails, completedItemsList

def checkEnemies(event, filePath, errorList, keyNames):
    event = event[0]
    if('Enemy' in event):
        if(keyNames.containsEnemy(event['Enemy']) != True):
            errorList.append(Error(ERRCODE.ITEM_ENEMY_DOES_NOT_EXIST, filePath+'/items.json',
                f"{event['Enemy']} enemy does not exist"))
    elif('Enemies' in event):
        for enemy in event['Enemies']:
            if(keyNames.containsEnemy(enemy) != True):
                errorList.append(Error(ERRCODE.ITEM_ENEMY_DOES_NOT_EXIST, filePath+'/items.json',
                    f"{enemy} enemy does not exist"))

def checkImage(image, filePath):
    imagesPath = filePath + '/images/' + image[0]
    if (os.path.isfile(imagesPath) != True):
        return False
    return True

def checkAudio(audio, filePath):
    audiosPath = filePath + '/audios/' + audio[0]
    if (os.path.isfile(audiosPath) != True):
        return False
    return True

def checkEventReferences(events, filePath, errorList, keyNames):
    for event in events:
        eventType = event['EventType']
        if(eventType == 'eGiveItem'):
            if(keyNames.containsItem(event['Item']) != True):
                errorList.append(Error(ERRCODE.ITEM_ITEM_DOES_NOT_EXIST, filePath+'/items.json',
                            f"{event['Item']} item does not exists"))
        elif(eventType == 'eLearnAttack'):
            if(keyNames.containsAttack(event['Attack']) != True):
                errorList.append(Error(ERRCODE.ITEM_ATTACK_DOES_NOT_EXIST, filePath+'/items.json',
                            f"{event['Attack']} attack does not exists"))
        elif(eventType == 'eStartBattle'):
            checkEnemies(event, filePath+'/items.json', errorList, keyNames)
        elif(eventType == 'eSendAudio'):
            if(checkAudio(event['AudioName'], filePath) == False):
                errorList.append(Error(ERRCODE.ITEM_AUDIO_DOES_NOT_EXIST, filePath+'/items.json',
                            f"{event['AudioName']} image does not exists"))
        elif(eventType == 'eSendImage'):
            if(checkImage(event['ImageName'], filePath) == False):
                errorList.append(Error(ERRCODE.ITEM_IMAGE_DOES_NOT_EXIST, filePath+'/items.json',
                            f"{event['ImageName']} image does not exists"))
        elif(eventType == 'eSendImageCollection'):
            for image in event['ImageCollection']:
                if(checkImage(image, filePath) == False):
                    errorList.append(Error(ERRCODE.ITEM_IMAGE_DOES_NOT_EXIST, filePath+'/items.json',
                                f"{event['ImageName']} image does not exists"))
        return

def checkItemReferences(itemList, filePath, keyNames):
    fails = list()
    for item in itemList:
        if('OnEquipEvents' in item):
            checkEventReferences(item['OnEquipEvents'], filePath, fails, keyNames)
        if('OnUnequipEvents' in item):
            checkEventReferences(item['OnUnequipEvents'], filePath, fails, keyNames)
    return len(fails) > 0, fails            

def checkUsableItemReferences(item, filePath, errorList):    
    for key in item['Key_Words']:
        if(checkEngineConstant(key['Value']['StatToChange'], "STAT") != True):
            errorList.append(Error(ERRCODE.ITEM_UNKNOWN_STAT, filePath+'/items.json',
                f"{key['Value']['StatToChange']} unknown stat"))
        if(checkEngineConstant(key['Value']['BehaviourType'], "BEHAVIOUR") != True):
            errorList.append(Error(ERRCODE.ITEM_UNKNOWN_BEHAVIOUR, filePath+'/items.json',
                f"{key['Value']['BehaviourType']} unknown behaviour"))

def checkEquipableItemReferences(item, filePath, errorList):
    if(checkEngineConstant(item['GearSlot'], "GEARSLOT") != True):
        errorList.append(Error(ERRCODE.ITEM_UNKNOWN_GEARSLOT, filePath+'/items.json',
            f"{item['GearSlot']} unknown gear slot"))
    
    for stat in item['StatModifiers']:
        if(checkEngineConstant(stat, "STAT") != True):
            errorList.append(Error(ERRCODE.ITEM_UNKNOWN_STAT, filePath+'/items.json',
                f"{stat} unknown stat"))


def checkEngineItemsReferences(itemList, filePath):
    fails = list()
    for item in itemList:
        if('Key_Words' in item):
            checkUsableItemReferences(item, filePath, fails)
        else: 
            checkEquipableItemReferences(item, filePath, fails)
    return len(fails) > 0, fails

def checkKeyWordsRepeated(itemList, filePath):
    fails = list()
    repeatedKeys = []
    for item in itemList:
        try:
            nKeyWords = len(item['Key_Words'])
            for i in range(nKeyWords):
                currentKey = item['Key_Words'][i]['Key']
                for j in range(nKeyWords):
                    if(i != j and currentKey == item['Key_Words'][j]['Key'] and currentKey not in repeatedKeys):
                        repeatedKeys.append(currentKey)
                        fails.append(Error(ERRCODE.ITEM_KEY_REPEATED, filePath,
                           f"{item['Key_Words'][j]['Key']} key is repeated in Key_Words at object named {item['Name']}"))
        except KeyError:
            pass
    
    return len(fails) > 0, fails
    
def checkInvalidFields(itemList):
    invalidFields = dict()
    for item in itemList:
        inv = [i for i in item.keys() if not isFieldValid(i, "Object")]
        if len(inv) > 0:
            invalidFields[item["Name"]] = inv
    return len(invalidFields) > 0, invalidFields

def checkAll(filesFolder, keyNames):
    print(f"\nChecking items...")
    filePath = filesFolder +'/items.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        itemList = json.loads(json_data.read())
    errorList = []

    # Exist keys
    res, fails, newList = checkItemsKeys(itemList, filePath)
    if res: itemList = newList
    for err in fails:
        errorList.append(err)
    print(f"Items missing keys errors: {len(fails)}")

    res, fails = checkKeyWordsRepeated(itemList, filePath)
    for err in fails:
        print(err.message)
        errorList.append(err)
    print(f"Items Key_Words keys repeated errors: {len(fails)}")
    
    res, fails = checkEngineItemsReferences(itemList, filePath)
    for err in fails:
        errorList.append(err)
    print(f"Items missing engine reference errors: {len(fails)}")

    res, fails = checkItemReferences(itemList, filesFolder, keyNames)
    for err in fails:
        errorList.append(err)
    print(f"Items missing reference errors: {len(fails)}")

    # Items with extra keys
    res, eMessages = checkInvalidFields(itemList)
    for k, v in eMessages.items():
        errorList.append(Error(ERRCODE.COMMON_INVALID_FIELD,
                        filePath, f'"{k}" has invalid fields {v}'))
    print(f"Item with invalid fields: {len(eMessages)}")

    return errorList