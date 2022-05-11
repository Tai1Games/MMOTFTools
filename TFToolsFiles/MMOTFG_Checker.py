import sys, os, io
import getopt
import json

#import mapaChecker
#import itemChecker
import directionsChecker
import EnemyChecker
#import attacksChecker

def displayHelp():
	print(
'''
Usage: python MMOTFG_Checker.py <filepath to checked directory> [options]

Usage example: python ../files/ -mid

Possible options:
	-h display this message
	-m check maps
	-i check items
	-d check directions
	-e check enemies
	-a attacks
''')

class KeyNamesRecord:
	availableNodes = []
	availableAttacks = []
	availableItems = []
	availableEnemies = []
	availableDirections = []

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
		for i in self.availableItems:
			print("\t-" + i)
		print("--------\nATTACKS")
		for i in self.availableAttacks:
			print("\t-" + i)
		print("--------\nENEMIES")
		for i in self.availableEnemies:
			print("\t-" + i)
		print("--------\nMAPNODES")
		for i in self.availableNodes:
			print("\t-" + i)
		print("--------\nDIRECTIONS")
		for i in self.availableDirections:
			print("\t-"+i[0], end=": ")
			print(*i[1:], sep=",")

	def __init__(self, pathToAssets):
		#---------------------
		#objetos
		with io.open(pathToAssets +'/items.json', encoding='utf-8-sig') as json_data:
			itemData = json.loads(json_data.read())

		for i in itemData:
			self.availableItems.append(i['Name'])
		#--------------------
		#ataques
		with io.open(pathToAssets+'/attacks.json', encoding='utf-8-sig') as json_data:
			attackData = json.loads(json_data.read())

		for i in attackData:
			self.availableAttacks.append(i['Name'])
		#--------------------
		#enemigos
		with io.open(pathToAssets+'/enemies.json', encoding='utf-8-sig') as json_data:
			enemyData = json.loads(json_data.read())

		for i in enemyData:
			self.availableEnemies.append(i['Name'])
		#--------------------
		#nodos
		with io.open(pathToAssets+'/map.json', encoding='utf-8-sig') as json_data:
			mapData = json.loads(json_data.read())

		for i in mapData:
			self.availableNodes.append(i['Name'])
		#----------------------
		#directions
		with io.open(pathToAssets+'/directionSynonyms.json', encoding='utf-8-sig') as json_data:
			directionsData = json.loads(json_data.read())

		for i in directionsData:
			synonyms = i["Synonyms"]
			synonyms.insert(0, i["Direction"])
			self.availableDirections.append(synonyms)
		#----------------------
		return

def main():
	#Check if user has input any arguments, if no arguments found execute all checks
	if len(sys.argv) == 1:
		displayHelp() #no 
	else:
		#Check that given filepath exists
		if not os.path.exists(sys.argv[1]):
			print("Given directory path is incorrect or doesn't exist")
			exit(1)

		#Get list of names
		keyNames = KeyNamesRecord(sys.argv[1])

		if len(sys.argv) == 2:
			directionsChecker.checkAll(sys.argv[1])
			print("Running all checks...")
			EnemyChecker.checkAll(sys.argv[1])
		else:
			#Get all relevant arguments
			arguments = sys.argv[2:]
			try:
				opts, args = getopt.getopt(arguments, "hmidea")

				for opt, arg in opts:
					if opt == "-m":
						#check maps
						print("placeholder")
					elif opt == "-i":
						#check items
						print("placeholder")
					elif opt == "-d":
						#check directions
						directionsChecker.checkAll(sys.argv[1])
					elif opt == "-e":
						EnemyChecker.checkAll(sys.argv[1])
					elif opt == "-a":
						#check items
						print("placeholder")
					elif opt == "-h":
						#display help
						displayHelp()
			except getopt.GetoptError:
				print("ERROR: Option not recognized")
				displayHelp()
				sys.exit(1)


if __name__ == "__main__":
	main()
