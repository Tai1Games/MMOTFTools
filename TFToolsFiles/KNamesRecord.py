import io
import json
import Error
from Error import ERRCODE

class KeyNamesRecord:
	availableNodes = []
	availableAttacks = []
	availableItems = []
	availableEnemies = []
	#-----------------------
	duplicatedNames = []

	def containsNode(self, n):
		if any(n in s for s in KeyNamesRecord.availableNodes):
			return True
			
	def containsAttack(self, a):
		if any(a in s for s in KeyNamesRecord.availableAttacks):
			return True

	def containsItem(self, i):
		if any(i in s for s in KeyNamesRecord.availableItems):
			return True

	def containsEnemy(self, e):
		if any(e in s for s in KeyNamesRecord.availableEnemies):
			return True

	def print(self):
		print("--------\nITEMS")
		for i in KeyNamesRecord.availableItems:
			print("  -" + i)
		print("--------\nATTACKS")
		for i in KeyNamesRecord.availableAttacks:
			print("  -" + i)
		print("--------\nENEMIES")
		for i in KeyNamesRecord.availableEnemies:
			print("  -" + i)
		print("--------\nMAPNODES")
		for i in KeyNamesRecord.availableNodes:
			print("  -" + i)

	def checkAll(self):
		for e in KeyNamesRecord.duplicatedNames: 
			print(e)

	def __init__(self, pathToAssets):
		#---------------------
		#objetos
		with io.open(pathToAssets +'/items.json', encoding='utf-8-sig') as json_data:
			itemData = json.loads(json_data.read())
		
		for i in itemData:
			if(KeyNamesRecord.containsItem(self, i['Name'])): KeyNamesRecord.duplicatedNames.append((ERRCODE.ITEM_NAME_DUPLICATED, pathToAssets + '/items.json', f'Item {i["Name"]} repeated'))
			KeyNamesRecord.availableItems.append(i['Name'])
		#--------------------
		#ataques
		with io.open(pathToAssets+'/attacks.json', encoding='utf-8-sig') as json_data:
			attackData = json.loads(json_data.read())

		for i in attackData:
			if(KeyNamesRecord.containsAttack(self, i['Name'])): KeyNamesRecord.duplicatedNames.append((ERRCODE.ATTACK_NAME_DUPLICATED, pathToAssets + '/attacks.json', f'Attack {i["Name"]} repeated'))
			KeyNamesRecord.availableAttacks.append(i['Name'])
		#--------------------
		#enemigos
		with io.open(pathToAssets+'/enemies.json', encoding='utf-8-sig') as json_data:
			enemyData = json.loads(json_data.read())

		for i in enemyData:
			if(KeyNamesRecord.containsEnemy(self, i['Name'])): KeyNamesRecord.duplicatedNames.append((ERRCODE.ENEMY_NAME_DUPLICATED, pathToAssets + '/enemies.json', f'Enemy {i["Name"]} repeated'))
			KeyNamesRecord.availableEnemies.append(i['Name'])
		#--------------------
		#nodos
		with io.open(pathToAssets+'/map.json', encoding='utf-8-sig') as json_data:
			mapData = json.loads(json_data.read())

		for i in mapData:
			if(KeyNamesRecord.containsNode(self, i['Name'])): KeyNamesRecord.duplicatedNames.append((ERRCODE.NODE_NAME_DUPLICATED, pathToAssets + '/map.json', f'Map node {i["Name"]} repeated'))
			KeyNamesRecord.availableNodes.append(i['Name'])
		#----------------------
		return
