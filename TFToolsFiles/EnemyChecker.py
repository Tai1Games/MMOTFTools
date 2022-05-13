import json
import io
import os
import Common
from Error import ERRCODE, Error
from Program import checkEngineConstant

def existingImage(enemyList, path):
    imagesPath = os.path.dirname(path) + '/images/'

    missingImages = [enemy["Name"] for enemy in enemyList
                     if "ImageName" not in enemy.keys() or
                     not os.path.isfile(imagesPath+enemy["ImageName"])]

    return len(missingImages), missingImages


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

    return len(fails), fails

# StatToChange, StatToDepend
def engineReferences(enemyList):
    fails = list()

    for item in enemyList:
        try:            
            for key, value in item.items():
                try:
                    statC = value["StatToChange"]
                    if not checkEngineConstant(statC, 'STAT'):
                        fails.append(f'{item["Name"]} has a reference to a unknown stat {statC}')
                except TypeError:
                    pass

                try:
                    statD = value["StatToDepend"]
                    if not checkEngineConstant(statD, 'STAT'):
                        fails.append(f'{item["Name"]} has a reference to a unknown stat {statD}')
                except TypeError:
                    pass

        except KeyError:
            pass
    return len(fails), fails

def statSize(enemyList):
    fails = []

    for item in enemyList:
        try:
            if len(item["Stats"]) != 4:
                fails.append(f'{item["Name"]} doesn\'t have 4 stats')
        except KeyError:
            try:
                # Has no Stats property
                fails.append(f'{item["Name"]} has no Stats block')
            except KeyError:
                # Doesn't event have a name lol
                fails.append(f"An enemy is malformed!")

    return len(fails), fails


def attacksSize(enemyList):
    fails = []

    for item in enemyList:
        try:
            if len(item["Attacks"]) < 1:
                fails.append(f'{item["Name"]} requires at least 1 attack')
        except KeyError:
            try:
                # Has no Attacks property
                fails.append(f'{item["Name"]} has no Attacks block')
            except KeyError:
                pass

    return len(fails), fails


def checkAll(filesFolder, namesRecord):
    print(f"Checking enemies...")
    filePath = filesFolder + '/enemies.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        enemyList = json.loads(json_data.read())

    errorList = []

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

    # json references
    res, eMessages = jsonReferences(enemyList, namesRecord)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_JSON_REFERENCE, filePath, f"{err}"))
    print(f"Json references check errors: {res}")

    # engine references
    res, eMessages = engineReferences(enemyList)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_ENGINE_REFERENCE, filePath, f"{err}"))
    print(f"Engine references check errors: {res}")

    # Missing images
    res, eMessages = existingImage(enemyList, filesFolder)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ENEMY_IMAGE_MISSING,
                         filePath, f'"{err}" has no image'))
    print(f"Missing image check errors: {res}")

    # Repeat keys
    RepeatKeysList = []
    for enemy in enemyList:
        # TODO return for html
        res, fails = Common.RepeatKeys(filePath, enemy)
        if len(fails) > 0:
            RepeatKeysList.append(fails)
    print(f"{len(RepeatKeysList)} repeat key errors found.")

    return errorList
