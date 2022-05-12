import json
import io
import os
import Common
from Error import ERRCODE, Error


def existingImage(enemyList,imagesPath):
    missingImages = [enemy["Name"] for enemy in enemyList
                    if "ImageName" not in enemy.keys() or
                    not os.path.isfile(imagesPath+enemy["ImageName"])]

    return len(missingImages), missingImages

def statSize(enemyList):
    fails = list()

    for item in enemyList:
        if len(item["Stats"]) != 4:
            fails.append(f'{item["Name"]} doesn\'t have 4 stats')

    return len(fails), fails

def attacksSize(enemyList):
    fails = list()

    for item in enemyList:
        if len(item["Attacks"]) < 1:
            fails.append(f'{item["Name"]} requires at least 1 attack')

    return len(fails), fails

def checkAll(filesFolder):
    print(f"Checking enemies...")
    filePath = filesFolder + '/enemies.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        enemyList = json.loads(json_data.read())

    errorList = []

    # Exist keys
    ExistKeysList = []
    # Contains objects with the required keys
    completedEnemiesList = []
    for enemy in enemyList:
        # TODO return for html
        res, fails = Common.ExistKeys(filePath, ["Stats", "Attacks", "ImageName"], [], enemy)
        if res > 0:
            ExistKeysList.append(fails)
        else:
            completedEnemiesList.append(enemy)
    enemyList = completedEnemiesList
    print(f"Enemies missing keys check errors: {len(ExistKeysList)}")

    # Statblock size
    res, eMessages = statSize(enemyList)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_STAT_SIZE, filePath, f"{err}"))
    print(f"Stat size check errors: {res}")

    # Attacks minimum size
    res, eMessages = attacksSize(enemyList)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_ATTACK_SIZE, filePath, f"{err}"))
    print(f"Attacks size check errors: {res}")

    #Missing images
    res, eMessages = existingImage(enemyList, os.path.dirname(filePath) + '/images/')
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_IMAGE_MISSING, filePath, f"{err} enemy has no image"))
    print(f"Missing image check errors: {res}")

    for err in errorList:
        print(err)
    # Repeat keys
    RepeatKeysList = []
    for enemy in enemyList:
        # TODO return for html
        res, fails = Common.RepeatKeys(filePath, enemy)
        if len(fails) > 0:
            RepeatKeysList.append(fails)
    print(f"{len(RepeatKeysList)} repeat key errors found.")