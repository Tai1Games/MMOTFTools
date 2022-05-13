import json
import io
import os
import Common
from Error import ERRCODE, Error


def existingImage(enemyList, path):
    imagesPath = os.path.dirname(path) + '/images/'

    missingImages = [enemy["Name"] for enemy in enemyList
                    if "ImageName" not in enemy.keys() or
                    not os.path.isfile(imagesPath+enemy["ImageName"])]

    return len(missingImages) > 0, missingImages


def jsonReferences(enemyList, namesRecord):
    fails = []

    for enemy in enemyList:
        # check items dropped
        if "DroppedItem" in enemy:
            if not namesRecord.containsItem(enemy["DroppedItem"]):
                fails.append(
                    f'"{enemy["Name"]}" dropped item "{enemy["DroppedItem"]}" doesn\'t exist')

        # check attacks
        if "Attacks" in enemy:
            for attack in enemy["Attacks"]:
                if not namesRecord.containsAttack(attack):
                    fails.append(
                        f'"{enemy["Name"]}" attack "{attack}" doesn\'t exist')

        # check referenced enemies onKill
        if "OnKill" in enemy:
            if "Enemy" in enemy["OnKill"]:
                # Janky motor it looks like
                if not namesRecord.containsEnemy(enemy["OnKill"]["Enemy"]):
                    fails.append(
                        f'"{enemy["OnKill"]["Enemy"]}" referenced by "{enemy["Name"]}" doesn\'t exist')
            elif "Enemies" in enemy["OnKill"]:
                for newEnemy in enemy["OnKill"]["Enemies"]:
                    if not namesRecord.containsEnemy(newEnemy):
                        fails.append(
                            f'"{newEnemy}" referenced by "{enemy["Name"]}" doesn\'t exist')

    return len(fails) > 0, fails


def statSize(enemyList):
    fails = []

    for item in enemyList:
        if len(item["Stats"]) != 4:
            fails.append(f'{item["Name"]} doesn\'t have 4 stats')

    return len(fails) > 0, fails


def attacksSize(enemyList):
    fails = []

    for item in enemyList:
        if len(item["Attacks"]) < 1:
            fails.append(f'{item["Name"]} requires at least 1 attack')

    return len(fails) > 0, fails


def checkAll(filesFolder, namesRecord):
    print(f"\nChecking Enemies...")
    errorList = list()
    filePath = filesFolder + '/enemies.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        enemyList = json.loads(json_data.read())

    # Exist keys
    # Contains objects with the required keys
    completedEnemiesList = []
    for idx, enemy in enumerate(enemyList):
        # TODO return for html
        res, eMessages = Common.ExistKeys(filePath, ["Stats", "Attacks", "ImageName"], [], enemy, idx)
        if res:
            for err in eMessages:
                errorList.append(Error(ERRCODE.OBJECT_KEY_MISSING, filePath, f"{err}"))
        else:
            completedEnemiesList.append(enemy)
    enemyList = completedEnemiesList
    print(f"Enemies missing keys errors: {len(errorList)}")

    # Statblock size
    res, eMessages = statSize(enemyList)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_STAT_SIZE, filePath, f"{err}"))
    print(f"Enemies Stat size errors: {len(eMessages)}")

    # Attacks minimum size
    res, eMessages = attacksSize(enemyList)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_ATTACK_SIZE, filePath, f"{err}"))
    print(f"Enemies Attacks size errors: {len(eMessages)}")

    # json references
    res, eMessages = jsonReferences(enemyList, namesRecord)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_JSON_REFERENCE, filePath, f"{err}"))
    print(f"Enemies Json references errors: {len(eMessages)}")

    # Missing images
    res, eMessages = existingImage(enemyList, filesFolder)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_IMAGE_MISSING,
                        filePath, f'"{err}" has no image'))
    print(f"Enemies missing image errors: {len(eMessages)}")

    # Repeat keys
    # repeatKeysLen = 0
    # for enemy in enemyList:
    #     # TODO return for html
    #     res, fails = Common.RepeatKeys(filePath, enemy)
    #     if res:
    #         for err in fails:
    #             errorList.append(err)
    #         repeatKeysLen += len(fails)
    # print(f"Enemies repeat keys errors: {repeatKeysLen}")

    return errorList
