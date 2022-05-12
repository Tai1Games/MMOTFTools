import json
import io
from os import path


def existingImage(filesFolder):
    fails = list()
    with io.open(filesFolder + '/enemies.json', encoding='utf-8-sig') as json_data:
        enemyList = json.loads(json_data.read())
    imagesPath = filesFolder + '/images/'

    missingImages = [enemy["Name"] for enemy in enemyList if not path.isfile(imagesPath+enemy["ImageName"])]

    return missingImages


def statSize(filesFolder):
    fails = list()
    with io.open(filesFolder + '/enemies.json', encoding='utf-8-sig') as json_data:
        enemyList = json.loads(json_data.read())
    for item in enemyList:
        try:
            if len(item["Stats"]) != 4:
                fails.append(f'{item["Name"]} doesn\'t have 4 stats')
        except KeyError:
            try:
                # Has no Stats property
                fails.append(f'{item["Name"]} has no stat block')
            except KeyError:
                # Doesn't event have a name lol
                fails.append(f"An item is malformed!")

    return fails


def checkAll(filesFolder):
    print(f"Stat size check errors: {len(statSize(filesFolder))}")
    print(f"Existing image check errors: {len(existingImage(filesFolder))}")
