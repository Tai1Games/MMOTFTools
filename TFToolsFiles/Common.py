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

    return len(errList), errList

def ExistKeys(filename, obligatoryKeys, atLeastOneKeys, object, idx):
    errList = []

    for key in obligatoryKeys:
        if key not in object:
            errList.append(Error(ERRCODE.OBJECT_KEY_MISSING, filename, 
                                f"Missing obligatory key {key} at object {idx}"))

    if len(atLeastOneKeys)>0:
        result = any(elem in object for elem in atLeastOneKeys)
        if(not result):
            errList.append(Error(ERRCODE.OBJECT_KEY_MISSING, filename, 
                                f"At least one key {atLeastOneKeys} at object {idx} is required"))

    return len(errList), errList
