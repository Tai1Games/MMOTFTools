import json
import io
import Common
from Error import ERRCODE, Error
from KNamesRecord import KeyNamesRecord
from Program import checkEngineConstant, isFieldValid


def negativeValues(attacksList):
    fails = list()

    for item in attacksList:

        try:
            # Negative value for Power
            if item["Power"] < 0:
                fails.append(
                    f'{item["Name"]} has a negative value at Power')
        except KeyError:
            pass

        try:
            # Negative value for MpCost
            if item["MpCost"] < 0:
                fails.append(
                    f'{item["Name"]} has a negative value at MpCost')
        except KeyError:
            pass

        try:
            # Negative value for Multiple
            if item["Multiple"] < 0:
                fails.append(
                    f'{item["Name"]} has a negative value at Multiple')
        except KeyError:
            pass

        try:
            # Negative value for FixedDamage
            if item["FixedDamage"] < 0:
                fails.append(
                    f'{item["Name"]} has a negative value at FixedDamage')
        except KeyError:
            pass

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

def checkAttacksKeys(attacksList, filePath):
    fails = list()

    # Contains objects with the required keys
    completedAttacksList = []

    for idx, attack in enumerate(attacksList):
        validAttack = True
        try:
            if attack["AttackType"] == "aScaled":
                res, errors = Common.ExistKeys(filePath, ["StatToScale"], [], attack, idx)
                if res:
                    validAttack = False
                    for err in errors:
                        fails.append(err)
            elif attack["AttackType"] == "aStatChanging":
                res, errors = Common.ExistKeys(filePath, ["StatToChange"], ["Multiple", "Change"], attack, idx)
                if res:
                    validAttack = False
                    for err in errors:
                        fails.append(err)
        except KeyError:
            pass

        if validAttack: completedAttacksList.append(attack)

    return len(fails) > 0, fails, completedAttacksList

def checkInvalidFields(attackList):
    invalidFields = dict()
    for attack in attackList:
        inv = [i for i in attack.keys() if not isFieldValid(i, "Attack")]
        if len(inv) > 0:
            invalidFields[attack["Name"]] = inv
    return len(invalidFields) > 0, invalidFields

def checkAll(filesFolder):
    print("\nChecking Attacks...")
    errorList = list()
    filePath = filesFolder + '/attacks.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        attacksList = json.loads(json_data.read())

    # Exist keys
    res, fails, newList = checkAttacksKeys(attacksList, filePath)
    if res: attacksList = newList
    for err in fails:
        errorList.append(err)
    print(f"Attacks missing keys errors: {len(fails)}")

    # Negative values
    res, eMessages = negativeValues(attacksList)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ATTACK_NEGATIVE_VALUE, filePath, f"{err}"))
    print(f"Attacks negative values errors: {len(eMessages)}")

    # Enemies with extra keys
    res, eMessages = checkInvalidFields(attacksList)
    for k, v in eMessages.items():
        errorList.append(Error(ERRCODE.COMMON_INVALID_FIELD,
                        filePath, f'"{k}" has invalid fields {v}'))
    print(f"Attacks with invalid fields: {len(eMessages)}")

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
    print(f"Attacks missing reference errors: {len(eMessages)}")
    
    return errorList
