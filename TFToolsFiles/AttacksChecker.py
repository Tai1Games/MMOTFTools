import json
import io
import Common
from Error import ERRCODE, Error

def negativeValues(attacksList):
	fails = list()

	for item in attacksList:
		try:
			# Negative value for MpCost
			if item["MpCost"] < 0:
				try:
					fails.append(
						f'{item["Name"]} has a negative value at MpCost')
				except KeyError:
					# Doesn't have a Name
					fails.append(f"An attack is malformed!")
					continue
		except KeyError:
			# MpCost field is not required
			pass

		try:
			# Negative value for Power
			if item["Power"] < 0:
				try:
					fails.append(
						f'{item["Name"]} has a negative value at Power')
				except KeyError:
					# Doesn't have a Name
					fails.append(f"An attack is malformed!")
					continue
		except KeyError:
			try:
				if item["Multiple"] < 0:
					try:
						fails.append(
							f'{item["Name"]} has a negative value at Multiple')
					except KeyError:
						# Doesn't have a Name
						fails.append(f"An attack is malformed!")
						continue
			except KeyError:
				try:
					fails.append(
						f'{item["Name"]} attack requires a Power or Multiple field!')
				except KeyError:
					# Doesn't have a Name
					fails.append(f"An attack is malformed!")
					continue
	return len(fails), fails


def checkAll(filesFolder):
	print("Checking Attacks...")
	filePath = filesFolder + '/attacks.json'
	with io.open(filePath, encoding='utf-8-sig') as json_data:
		attacksList = json.loads(json_data.read())

	errorList = []

	# Negative values
	res, eMessages = negativeValues(attacksList)
	for err in eMessages:
		errorList.append(Error(ERRCODE.ATTACK_NEGATIVE_VALUE, filePath, f"{err}"))
	print(f"Attacks negative values check errors: {res}")

	# Repeat keys
	RepeatKeysList = []
	for attack in attacksList:
		# TODO return for html
		res, fails = Common.RepeatKeys(filePath, attack)
		if len(fails) > 0:
			RepeatKeysList.append(fails)
	print(f"{res} repeat key errors found.")
	return errorList
