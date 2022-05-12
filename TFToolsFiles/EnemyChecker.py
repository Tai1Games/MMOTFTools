import Common, json, io
from Error import ERRCODE, Error

def statSize(enemyList):
	fails = list()
	
	for item in enemyList:
		try:
			if len(item["Stats"]) != 4:
				fails.append(f'{item["Name"]} doesn\'t have 4 stats')
		except KeyError:
			try:
				#Has no Stats property
				fails.append(f'{item["Name"]} has no Stats block')
			except KeyError:
				#Doesn't event have a name lol
				fails.append(f"An enemy is malformed!")

	return len(fails), fails

def attacksSize(path):
	fails = list()
	with io.open(path, encoding='utf-8-sig') as json_data:
		enemyList = json.loads(json_data.read())

	for item in enemyList:
		try:
			if len(item["Attacks"]) < 1:
				fails.append(f'{item["Name"]} requires at least 1 attack')
		except KeyError:
			try:
				#Has no Attacks property
				fails.append(f'{item["Name"]} has no Attacks block')
			except KeyError:
				pass

	return len(fails), fails

def checkAll(filesFolder):
	print(f"Checking enemies...")
	with io.open(filesFolder +'/enemies.json', encoding='utf-8-sig') as json_data:
		enemyList = json.loads(json_data.read())

	errorList = []

	# Statblock size
	res, eMessages = statSize(enemyList)
	for err in eMessages:
		errorList.append(Error(ERRCODE.ENEMY_STAT_SIZE, "enemies.json", f"{err}"))
	print(f"Stat size check errors: {res}")

	# Attacks minimum size
	res, eMessages = attacksSize(enemyList)
	for err in eMessages:
		errorList.append(Error(ERRCODE.ENEMY_ATTACK_SIZE, "enemies.json", f"{err}"))
	print(f"Attacks size check errors: {res}")

	# Repeat keys
	RepeatKeysList = []
	for enemy in enemyList:
		# TODO return for html
		res, fails = Common.RepeatKeys("enemies.json", enemy)
		if len(fails) > 0:
			RepeatKeysList.append(fails)
	print(f"{len(RepeatKeysList)} repeat key errors found.")
