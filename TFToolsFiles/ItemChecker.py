import Common, io, json

def checkAll(filesFolder):
	print(f"Checking items...")
	with io.open(filesFolder +'/items.json', encoding='utf-8-sig') as json_data:
		itemList = json.loads(json_data.read())


	# Repeat keys
	RepeatKeysList = []
	for item in itemList:
		# TODO return for html
		res, fails = Common.RepeatKeys("items.json", item)
		if len(fails) > 0:
			RepeatKeysList.append(fails)
	print(f"{len(RepeatKeysList)} repeat key errors found.")