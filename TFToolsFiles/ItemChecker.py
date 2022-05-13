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
            


def checkAll(filesFolder, keyNames):
    print(f"Checking items...")
    filePath = filesFolder +'/items.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        itemList = json.loads(json_data.read())

    errorList = []
    checkItemReferences(itemList, filesFolder, errorList, keyNames)

    print(f"{len(errorList)} items errors found.")

    return errorList