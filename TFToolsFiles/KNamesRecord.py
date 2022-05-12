import io
import json
from Error import ERRCODE, Error

class KeyNamesRecord:
    availableNodes = []
    availableAttacks = []
    availableItems = []
    availableEnemies = []
    #-----------------------
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
        for e in self.duplicatedNames: 
            print(e.errCode, end = ' ')
            print("@" + e.file + ": " + e.message)
        return self.duplicatedNames

    def __init__(self, pathToAssets):
        #---------------------
        #objetos
        with io.open(pathToAssets +'/items.json', encoding='utf-8-sig') as json_data:
            itemData = json.loads(json_data.read())
        
        for idx, i in enumerate(itemData):
            try:
                i['Name']
            except KeyError:
                raise Exception(f'Missing key Name from Items file at Item {idx}')
            if(self.containsItem(i['Name'])): self.duplicatedNames.append(Error(ERRCODE.ITEM_NAME_DUPLICATED, pathToAssets + '/items.json', f'Item {i["Name"]} repeated'))
            self.availableItems.append(i['Name'])
        #--------------------
        #ataques
        with io.open(pathToAssets+'/attacks.json', encoding='utf-8-sig') as json_data:
            attackData = json.loads(json_data.read())

        for idx, i in enumerate(attackData):
            try:
                i['Name']
            except KeyError:
                raise Exception(f'Missing key Name from Attacks file at Attack {idx}')
            if(self.containsAttack(i['Name'])): self.duplicatedNames.append(Error(ERRCODE.ATTACK_NAME_DUPLICATED, pathToAssets + '/attacks.json', f'Attack {i["Name"]} repeated'))
            self.availableAttacks.append(i['Name'])
        #--------------------
        #enemigos
        with io.open(pathToAssets+'/enemies.json', encoding='utf-8-sig') as json_data:
            enemyData = json.loads(json_data.read())

        for idx, i in enumerate(enemyData):
            try:
                i['Name']
            except KeyError:
                raise Exception(f'Missing key Name from Enemies file at Enemy {idx}')
            if(self.containsEnemy(i['Name'])): self.duplicatedNames.append(Error(ERRCODE.ENEMY_NAME_DUPLICATED, pathToAssets + '/enemies.json', f'Enemy {i["Name"]} repeated'))
            self.availableEnemies.append(i['Name'])
        #--------------------
        #nodos
        with io.open(pathToAssets+'/map.json', encoding='utf-8-sig') as json_data:
            mapData = json.loads(json_data.read())

        for idx, i in enumerate(mapData):
            try:
                i['Name']
            except KeyError:
                raise Exception(f'Missing key Name from Map file at Node {idx}')
            if(self.containsNode(i['Name'])): self.duplicatedNames.append(Error(ERRCODE.NODE_NAME_DUPLICATED, pathToAssets + '/map.json', f'Map node {i["Name"]} repeated'))
            self.availableNodes.append(i['Name'])
        #----------------------
        return
