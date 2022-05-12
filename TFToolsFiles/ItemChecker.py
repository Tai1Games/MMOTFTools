import Common, io, json

def checkAll(filesFolder):
    print(f"\nChecking Items...")
    errorList = list()
    filePath = filesFolder + '/items.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        itemList = json.loads(json_data.read())

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