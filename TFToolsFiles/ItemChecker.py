from tabnanny import check
import Common, io, json
from Error import ERRCODE, Error
import Program
import Common
import os


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

def checkEventReferences(event, filePath, errorList, keyNames):
    eventType = event[0]['EventType']
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
        if(checkAudio(event[0]['AudioName'], filePath) == False):
            errorList.append(Error(ERRCODE.ITEM_AUDIO_DOES_NOT_EXIST, filePath+'/items.json',
                          f"{event[0]['AudioName']} image does not exists"))
    elif(eventType == 'eSendImage'):
        if(checkImage(event[0]['ImageName'], filePath) == False):
            errorList.append(Error(ERRCODE.ITEM_IMAGE_DOES_NOT_EXIST, filePath+'/items.json',
                          f"{event[0]['ImageName']} image does not exists"))
    elif(eventType == 'eSendImageCollection'):
        for image in event['ImageCollection']:
            if(checkImage(image, filePath) == False):
                errorList.append(Error(ERRCODE.ITEM_IMAGE_DOES_NOT_EXIST, filePath+'/items.json',
                            f"{event[0]['ImageName']} image does not exists"))
    return

def checkItemReferences(itemList, filePath, errorList, keyNames):
    for item in itemList:
        if('OnEquipEvents' in item):
            checkEventReferences(item['OnEquipEvents'], filePath, errorList, keyNames)
        if('OnUnequipEvents' in item):
            checkEventReferences(item['OnUnequipEvents'], filePath, errorList, keyNames)
            
def checkKeyWords(itemList, filePath, errorList):
    for item in itemList:
        if('Key_Words' in item):
            for i in range(0, len(item['Key_Words'])):
                for j in range(0, len(item['Key_Words'])):
                    if(i != j and item['Key_Words'][i]['Key'] == item['Key_Words'][j]['Key']):
                        errorList.append(Error(ERRCODE.ITEM_KEY_REPEATED, filePath+'/items.json',
                           f"{item['Key_Words'][j]['Key']} key is repeated"))



def checkUsableItemReferences(item, filePath, errorList):    
    for key in item['Key_Words']:
        if(Program.checkEngineConstant(key['Value']['StatToChange'], "STAT") != True):
            errorList.append(Error(ERRCODE.ITEM_UNKNOWN_STAT, filePath+'/items.json',
                f"{key['Value']['StatToChange']} unknown stat"))
        if(Program.checkEngineConstant(key['Value']['BehaviourType'], "BEHAVIOUR") != True):
            errorList.append(Error(ERRCODE.ITEM_UNKNOWN_BEHAVIOUR, filePath+'/items.json',
                f"{key['Value']['BehaviourType']} unknown behaviour"))

def checkEquipableItemReferences(item, filePath, errorList):
    if(Program.checkEngineConstant(item['GearSlot'], "GEARSLOT") != True):
        errorList.append(Error(ERRCODE.ITEM_UNKNOWN_GEARSLOT, filePath+'/items.json',
            f"{item['GearSlot']} unknown gear slot"))
    
    for stat in item['StatModifiers']:
        if(Program.checkEngineConstant(stat, "STAT") != True):
            errorList.append(Error(ERRCODE.ITEM_UNKNOWN_STAT, filePath+'/items.json',
                f"{stat} unknown stat"))


def checkEngineItemsReferences(itemList, filePath, errorList):
    for item in itemList:
        if('Key_Words' in item):
            checkUsableItemReferences(item, filePath, errorList)
        else: 
            checkEquipableItemReferences(item, filePath, errorList)


def checkAll(filesFolder, keyNames):
    print(f"Checking items...")
    filePath = filesFolder +'/items.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        itemList = json.loads(json_data.read())

    errorList = []
    checkItemReferences(itemList, filesFolder, errorList, keyNames)
    checkKeyWords(itemList, filePath, errorList)
    checkEngineItemsReferences(itemList, filePath, errorList)

    print(f"{len(errorList)} items errors found.")

    return errorList