import json
import io

def negativeValues(filesFolder):
	fails = list()
	with io.open(filesFolder +'/attacks.json', encoding='utf-8-sig') as json_data:
		attacksList = json.loads(json_data.read())

	for item in attacksList:
		try:
			#Negative value for MpCost
			if item["MpCost"] < 0:
				try:
					fails.append(f'{item["Name"]} has a negative value at MpCost')
				except KeyError:
					#Doesn't have a Name
					fails.append(f"An attack is malformed!")
					continue
		except KeyError:
			#MpCost field is not required
			pass

		try:
			#Negative value for Power
			if item["Power"] < 0:
				try:
					fails.append(f'{item["Name"]} has a negative value at Power')
				except KeyError:
					#Doesn't have a Name
					fails.append(f"An attack is malformed!")
					continue
		except KeyError:
			try:
				if item["Multiple"] < 0:
					try:
						fails.append(f'{item["Name"]} has a negative value at Multiple')
					except KeyError:
						#Doesn't have a Name
						fails.append(f"An attack is malformed!")
						continue
			except KeyError:
				try:
					fails.append(f'{item["Name"]} attack requires a Power or Multiple field!')
				except KeyError:
					#Doesn't have a Name
					fails.append(f"An attack is malformed!")
					continue
	return len(fails), fails

def checkAll(filesFolder):
	res, fails = negativeValues(filesFolder)
	print(f"Attacks negative values check errors: {res}")
	print(fails)