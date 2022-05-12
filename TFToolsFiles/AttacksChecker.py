import json
import io
import Common
from Error import ERRCODE, Error

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

    return len(fails), fails


def checkAll(filesFolder):
    print("Checking Attacks...")
    filePath = filesFolder + '/attacks.json'
    with io.open(filePath, encoding='utf-8-sig') as json_data:
        attacksList = json.loads(json_data.read())

    errorList = []

    # Exist keys
    ExistKeysList = []
    # Contains objects with the required keys
    completedAttacksList = []
    for attack in attacksList:
        # TODO return for html
        res, fails = Common.ExistKeys(filePath, [], ["Power", "Multiple"], attack)
        if res > 0:
            ExistKeysList.append(fails)
        else:
            completedAttacksList.append(attack)
    attacksList = completedAttacksList
    print(f"Attacks missing keys check errors: {len(ExistKeysList)}")

    # Negative values
    res, eMessages = negativeValues(attacksList)
    for err in eMessages:
        errorList.append(Error(ERRCODE.ATTACK_NEGATIVE_VALUE, filePath, f"{err}"))
    print(f"Attacks negative values check errors: {res}")

    # Repeat keys
    RepeatKeysList = []
    for attack in attacksList:
        # TODO return for html
        res, fails = Common.RepeatKeys(filePath, attack)
        if len(fails) > 0:
            RepeatKeysList.append(fails)
    print(f"{res} repeat key errors found.")