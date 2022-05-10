import enum
import json



def checkEngineConstant(constToCheck, type):
    if(type == 'EVENT'):
        if any(constToCheck in s for s in engine_constants['Events']):
             return True
    elif(type == 'STAT'):
        if any(constToCheck in s for s in engine_constants['Stats']):
             return True
    elif(type == 'GEARSLOT'):
        if any(constToCheck in s for s in engine_constants['GearSlots']):
             return True
    return False

#----------------------------------------------------------

with open('TFToolsFiles/EngineConstants.json', 'r') as f:
    engine_constants = json.load(f)

if(checkEngineConstant("Cock", "GEARSLOT")): print("OUI VEGGI GUD DIS MAP")
else: print("OH NON NON DIS MAP IS BEGGRI BAD U SEE")