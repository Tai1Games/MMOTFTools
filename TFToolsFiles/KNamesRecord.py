import io
import json

class KeyNamesRecord:
	availableNodes = []
	availableAttacks = []
	availableItems = []
	availableEnemies = []
	#-----------------------
	duplicatedNodes = [] #Lo dejo todos separados porque será más fácil hacer el output en HTML de esta manera
	duplicatedAttacks = []
	duplicatedItems = []
	duplicatedEnemies = []

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
		print("Checking for repeated keyNames...")	
		for i in KeyNamesRecord.duplicatedItems: print(i)
		for i in KeyNamesRecord.duplicatedAttacks: print(i)
		for i in KeyNamesRecord.duplicatedEnemies: print(i)
		for i in KeyNamesRecord.duplicatedNodes: print(i)

	def __init__(self, pathToAssets):
		#---------------------
		#objetos
		with io.open(pathToAssets +'/items.json', encoding='utf-8-sig') as json_data:
			itemData = json.loads(json_data.read())
		
		for i in itemData:
			if(KeyNamesRecord.containsItem(self, i['Name'])): KeyNamesRecord.duplicatedItems.append(f'Item {i["Name"]} is duplicated')
			KeyNamesRecord.availableItems.append(i['Name'])
		#--------------------
		#ataques
		with io.open(pathToAssets+'/attacks.json', encoding='utf-8-sig') as json_data:
			attackData = json.loads(json_data.read())

		for i in attackData:
			if(KeyNamesRecord.containsAttack(self, i['Name'])): KeyNamesRecord.duplicatedAttacks.append(f'Attack {i["Name"]} is duplicated')
			KeyNamesRecord.availableAttacks.append(i['Name'])
		#--------------------
		#enemigos
		with io.open(pathToAssets+'/enemies.json', encoding='utf-8-sig') as json_data:
			enemyData = json.loads(json_data.read())

		for i in enemyData:
			if(KeyNamesRecord.containsEnemy(self, i['Name'])): KeyNamesRecord.duplicatedEnemies.append(f'Enemy {i["Name"]} is duplicated')
			KeyNamesRecord.availableEnemies.append(i['Name'])
		#--------------------
		#nodos
		with io.open(pathToAssets+'/map.json', encoding='utf-8-sig') as json_data:
			mapData = json.loads(json_data.read())

		for i in mapData:
			if(KeyNamesRecord.containsNode(self, i['Name'])): KeyNamesRecord.duplicatedNodes.append(f'Node {i["Name"]} is duplicated')
			KeyNamesRecord.availableNodes.append(i['Name'])
		#----------------------
		return
