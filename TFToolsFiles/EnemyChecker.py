import Common, json, io

def statSize(enemyList):
	fails = list()
	
	for item in enemyList:
		try:
			if len(item["Stats"]) != 4:
				fails.append(f'{item["Name"]} doesn\'t have 4 stats')
		except KeyError:
			try:
				#Has no Stats property
				fails.append(f'{item["Name"]} has no stat block')
			except KeyError:
				#Doesn't event have a name lol
				fails.append(f"An item is malformed!")

	return fails

def checkAll(filesFolder):
	print(f"Checking enemies...")
	with io.open(filesFolder +'/enemies.json', encoding='utf-8-sig') as json_data:
		enemyList = json.loads(json_data.read())

	#Statblock size
	print(f"Stat size check errors: {len(statSize(enemyList))}")

	# Repeat keys
	RepeatKeysList = []
	for enemy in enemyList:
		# TODO return for html
		res, fails = Common.RepeatKeys("enemies.json", enemy)
		if len(fails) > 0:
			RepeatKeysList.append(fails)
	print(f"{len(RepeatKeysList)} repeat key errors found.")