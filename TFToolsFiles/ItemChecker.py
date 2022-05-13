import Common, io, json

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

def checkAll(filesFolder):
    print(f"\nChecking Items...")
    errorList = list()
    filePath = filesFolder + '/items.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        itemList = json.loads(json_data.read())

    # Exist keys
    res, fails, newList = checkItemsKeys(itemList, filePath)
    if res: itemList = newList
    for err in fails:
        print(err.message)
        errorList.append(err)
    print(f"Items missing keys errors: {len(fails)}")

    # Repeat keys
    repeatKeysLen = 0
    for item in itemList:
        # TODO return for html
        res, fails = Common.RepeatKeys(filePath, item)
        if res:
            for err in fails:
                errorList.append(err)
            repeatKeysLen += len(fails)
    print(f"Items repeat keys errors: {repeatKeysLen}")

    return errorList