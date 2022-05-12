import Common, io, json

def checkAll(filesFolder):
	print(f"Checking maps...")
	with io.open(filesFolder +'/map.json', encoding='utf-8-sig') as json_data:
		nodeList = json.loads(json_data.read())


	# Repeat keys
	RepeatKeysList = []
	for node in nodeList:
		# TODO return for html
		res, fails = Common.RepeatKeys("maps.json", node)
		if len(fails) > 0:
			RepeatKeysList.append(fails)
	print(f"{len(RepeatKeysList)} repeat key errors found.")
	
	return fails