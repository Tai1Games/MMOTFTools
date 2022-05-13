from Error import Error, ERRCODE

def RepeatKeys(filename, object):
    errList = []
    knownKeys = []

    for key in object:
        if key in knownKeys:
            print(f"duplicate key {key}")
            errList.append(Error(ERRCODE.OBJECT_KEYS_DUPLICATED, filename,
                                f"Duplicate key {key} found in object"))
        else:
            knownKeys.append(key)

    return len(errList) > 0, errList

# The object must include all the keys from obligatoryKeys and at least one key from atLeastOneKeys
def ExistKeys(filename, obligatoryKeys, atLeastOneKeys, object, idx):
    errList = []

    for key in obligatoryKeys:
        if key not in object:
            errList.append(Error(ERRCODE.OBJECT_KEY_MISSING, filename, 
                                f"Missing obligatory key {key} at object {idx}"))

    if len(atLeastOneKeys) > 0:
        result = any(elem in object for elem in atLeastOneKeys)
        if(not result):
            errList.append(Error(ERRCODE.OBJECT_KEY_MISSING, filename, 
                                f"At least one key {atLeastOneKeys} at object {idx} is required"))

    return len(errList) > 0, errList

# The object must include all the keys from obligatoryKeys and at least one key from atLeastOneKeys
def ExistKeysOnEvents(filePath, onEventsKeys, object, idx):
    errList = []

    for key in onEventsKeys:
        try:
            for idxE, event in enumerate(object[key]):
                res, errors = ExistKeys(filePath, ["EventType"], [], event, idx)
                if res:
                    for err in errors:
                        err.message += f", at event {idxE} from {key}"
                        errList.append(err)
                else:
                    if event["EventType"] == "eSendText":
                        res, errors = ExistKeys(filePath, ["Description"], [], event, idx)
                        if res:
                            for err in errors:
                                err.message += f", at event {idxE} from {key}"
                                errList.append(err)
                    elif event["EventType"] == "eSendImage":
                        res, errors = ExistKeys(filePath, ["ImageName"], [], event, idx)
                        if res:
                            for err in errors:
                                err.message += f", at event {idxE} from {key}"
                                errList.append(err)
                    elif event["EventType"] == "eSendImageCollection":
                        res, errors = ExistKeys(filePath, ["ImagesNames"], [], event, idx)
                        if res:
                            for err in errors:
                                err.message += f", at event {idxE} from {key}"
                                errList.append(err)
                    elif event["EventType"] == "eGiveItem":
                        res, errors = ExistKeys(filePath, ["ItemLots"], [], event, idx)
                        if res:
                            for err in errors:
                                err.message += f", at event {idxE} from {key}"
                                errList.append(err)
                        else:
                            for itemLot in event["ItemLots"]:
                                res, errors = ExistKeys(filePath, ["Item"], [], itemLot, idx)
                                if res:
                                    for err in errors:
                                        err.message += f", at event {idxE} from {key}"
                                        errList.append(err)
                    elif event["EventType"] == "eSetFlag":
                        res, errors = ExistKeys(filePath, ["Name","SetAs"], [], event, idx)
                        if res:
                            for err in errors:
                                err.message += f", at event {idxE} from {key}"
                                errList.append(err)
                    elif event["EventType"] == "eSendAudio":
                        res, errors = ExistKeys(filePath, ["AudioName"], [], event, idx)
                        if res:
                            for err in errors:
                                err.message += f", at event {idxE} from {key}"
                                errList.append(err)
                    elif event["EventType"] == "eStartBattle":
                        res, errors = ExistKeys(filePath, [], ["Enemy","Enemies"], event, idx)
                        if res:
                            for err in errors:
                                err.message += f", at event {idxE} from {key}"
                                errList.append(err)
        except KeyError:
            pass

    return len(errList) > 0, errList
