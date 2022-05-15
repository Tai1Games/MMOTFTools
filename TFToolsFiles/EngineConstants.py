import json

def checkEngineConstant(constToCheck, type):
    if(type == 'EVENTTYPE'):
        if any(constToCheck in s for s in engine_constants['EventsType']):
             return True
    elif(type == 'STAT'):
        if any(constToCheck in s for s in engine_constants['Stats']):
             return True
    elif(type == 'GEARSLOT'):
        if any(constToCheck in s for s in engine_constants['GearSlots']):
             return True
    elif(type == 'EVENT'):
        if any(constToCheck in s for s in engine_constants['Events']):
             return True
    elif(type == 'ATTACKTYPE'):
        if any(constToCheck in s for s in engine_constants['AttackTypes']):
             return True
    elif(type == 'BEHAVIOUR'):
        if any(constToCheck in s for s in engine_constants['BehaviourType']):
             return True
    return False

def isFieldValid(fieldToCheck, type):
    try:
        return fieldToCheck in engine_constants["PossibleFields"][type]\
               or fieldToCheck in engine_constants["PossibleFields"]["Common"]
    except:
        return False

def getEngineConstants(constantsToGet):
    if(constantsToGet == "EVENTS"):
        return engine_constants['Events']
    elif(constantsToGet in engine_constants):
        return engine_constants[constantsToGet]

#----------------------------------------------------------

with open('./EngineConstants.json', 'r') as f:
    engine_constants = json.load(f)