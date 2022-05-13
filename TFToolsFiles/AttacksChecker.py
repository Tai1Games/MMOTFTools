import json
import io
import Common
from Error import ERRCODE, Error
from KNamesRecord import KeyNamesRecord
from Program import checkEngineConstant


def negativeValues(attacksList):
    fails = list()

    for item in attacksList:
        try:
            # Negative value for MpCost
            if item["MpCost"] < 0:
                fails.append(
                    f'{item["Name"]} has a negative value at MpCost')
        except KeyError:
            # MpCost field is not required
            pass

        try:
            # Negative value for Power
            if item["Power"] < 0:
                fails.append(
                    f'{item["Name"]} has a negative value at Power')
        except KeyError:
            if item["Multiple"] < 0:
                fails.append(
                    f'{item["Name"]} has a negative value at Multiple')

    return len(fails) > 0, fails

def checkReferences(attacksList):
    fails = list()

    for item in attacksList:
        try:
            # stat change 
            statC = item["StatToChange"]

            if not checkEngineConstant(statC, 'STAT'):
                fails.append(f'{item["Name"]} has a reference to a unknown stat {statC}')
        except KeyError:
            pass

        try:
            # stat scale
            statS = item["StatToScale"]
           
            if not checkEngineConstant(statS, 'STAT'):
                fails.append(f'{item["Name"]} has a reference to a unknown stat {statS}')
        except KeyError:
            pass    

        try:
            # attack type exist            
            if not checkEngineConstant(item["AttackType"], 'ATTACKTYPE'):
                fails.append(f'{item["Name"]} has a reference to a unknown attackType {item["AttackType"]}')          
        except KeyError:
            pass

    return len(fails) > 0, fails

def checkAll(filesFolder):
    print("\nChecking Attacks...")
    errorList = list()
    filePath = filesFolder + '/attacks.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        attacksList = json.loads(json_data.read())

    # Exist keys
    # Contains objects with the required keys
    completedAttacksList = []
    for idx, attack in enumerate(attacksList):
        # TODO return for html
        res, fails = Common.ExistKeys(filePath, [], ["Power", "Multiple"], attack, idx)
        if res:
            for err in fails:
                errorList.append(err)
        else:
            completedAttacksList.append(attack)
    attacksList = completedAttacksList
    print(f"Attacks missing keys errors: {len(errorList)}")

    # Negative values
    res, eMessages = negativeValues(attacksList)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ATTACK_NEGATIVE_VALUE, filePath, f"{err}"))
    print(f"Attacks negative values errors: {len(eMessages)}")

    # Repeat keys
    # repeatKeysLen = 0
    # for attack in attacksList:
    #     # TODO return for html
    #     res, fails = Common.RepeatKeys(filePath, attack)
    #     if res:
    #         for err in fails:
    #             errorList.append(err)
    #         repeatKeysLen += len(fails)
    # print(f"Attacks repeat keys errors: {repeatKeysLen}")

    # Missing references
    res, eMessages = checkReferences(attacksList)
    for err in eMessages:
        errorList.append(
            Error(ERRCODE.ATTACK_MISSING_REFERENCES, filePath, f"{err}"))
    print(f"Missing references in attacks: {len(eMessages)}")
    
    return errorList
