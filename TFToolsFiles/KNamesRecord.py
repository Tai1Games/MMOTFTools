import io
import json
from Error import ERRCODE, Error

class KeyNamesRecord:
    availableNodes = []
    availableAttacks = []
    availableItems = []
    availableEnemies = []
    #-----------------------
    missingNames = []
    duplicatedNames = []

    def containsNode(self, n):
        if n in self.availableNodes:
            return True
            
    def containsAttack(self, a):
        if a in self.availableAttacks:
            return True

    def containsItem(self, i):
        if i in self.availableItems:
            return True

    def containsEnemy(self, e):
        if e in self.availableEnemies:
            return True

    def print(self):
        print("--------\nITEMS")
        for i in self.availableItems:
            print("  -" + i)
        print("--------\nATTACKS")
        for i in self.availableAttacks:
            print("  -" + i)
        print("--------\nENEMIES")
        for i in self.availableEnemies:
            print("  -" + i)
        print("--------\nMAPNODES")
        for i in self.availableNodes:
            print("  -" + i)

    def checkAll(self):
        print('\033[91m')
        for e in self.missingNames: 
            print(e.errCode, end = ' ')
            print("@" + e.file + ": " + e.message)
        for e in self.duplicatedNames: 
            print(e.errCode, end = ' ')
            print("@" + e.file + ": " + e.message)
        print('\033[0m')
        return len(self.missingNames) == 0 and len(self.duplicatedNames) == 0

    def __init__(self, pathToAssets):
        #---------------------
        #objetos
        with io.open(pathToAssets +'/items.json', encoding='utf-8-sig') as json_data:
            itemData = json.loads(json_data.read())
        
        for idx, i in enumerate(itemData):
            try:
                if(self.containsItem(i['Name'])): self.duplicatedNames.append(Error(ERRCODE.ITEM_NAME_DUPLICATED, pathToAssets + '/items.json', f'Item {i["Name"]} repeated'))
                self.availableItems.append(i['Name'])
            except KeyError:
                self.missingNames.append(Error(ERRCODE.ITEM_NAME_MISSING, pathToAssets + '/items.json', f'Missing key Name from Items file at Item object {idx}'))
        #--------------------
        #ataques
        with io.open(pathToAssets+'/attacks.json', encoding='utf-8-sig') as json_data:
            attackData = json.loads(json_data.read())

        for idx, i in enumerate(attackData):
            try:
                if(self.containsAttack(i['Name'])): self.duplicatedNames.append(Error(ERRCODE.ATTACK_NAME_DUPLICATED, pathToAssets + '/attacks.json', f'Attack {i["Name"]} repeated'))
                self.availableAttacks.append(i['Name'])
            except KeyError:
                self.missingNames.append(Error(ERRCODE.ATTACK_NAME_MISSING, pathToAssets + '/items.json', f'Missing key Name from Attacks file at Attack object {idx}'))
        #--------------------
        #enemigos
        with io.open(pathToAssets+'/enemies.json', encoding='utf-8-sig') as json_data:
            enemyData = json.loads(json_data.read())

        for idx, i in enumerate(enemyData):
            try:
                if(self.containsEnemy(i['Name'])): self.duplicatedNames.append(Error(ERRCODE.ENEMY_NAME_DUPLICATED, pathToAssets + '/enemies.json', f'Enemy {i["Name"]} repeated'))
                self.availableEnemies.append(i['Name'])
            except KeyError:
                self.missingNames.append(Error(ERRCODE.ENEMY_NAME_MISSING, pathToAssets + '/items.json', f'Missing key Name from Enemies file at Enemy object {idx}'))
        #--------------------
        #nodos
        with io.open(pathToAssets+'/mapejemplo.json', encoding='utf-8-sig') as json_data:
            mapData = json.loads(json_data.read())

        for idx, i in enumerate(mapData):
            try:
                if(self.containsNode(i['Name'])): self.duplicatedNames.append(Error(ERRCODE.NODE_NAME_DUPLICATED, pathToAssets + '/map.json', f'Map node {i["Name"]} repeated'))
                self.availableNodes.append(i['Name'])
            except KeyError:
                self.missingNames.append(Error(ERRCODE.NODE_NAME_MISSING, pathToAssets + '/items.json', f'Missing key Name from Map file at Node object {idx}'))
        #----------------------
        return
