import json
import io
from Error import ERRCODE

def checkConnectingNodes(roomsList, filePath, errorList, keyNames):
	for room in roomsList:
		for n in room['NodeConnections']:
			name = room['NodeConnections'][n]['ConnectingNode']

			if(keyNames.containsNode(name) != True):
				errorList.append((ERRCODE.NODE_DOES_NOT_EXISTS, filePath,
						  f"{name} node does not exists"))

						  

def checkAll(filesFolder, keyNames):
	errorList = list()
	filePath = filesFolder + '/mapejemplo.json'
	with io.open(filePath, encoding='utf-8-sig') as json_data:
		roomsList = json.loads(json_data.read())
	

	checkConnectingNodes(roomsList, filePath, errorList, keyNames)



	for err in errorList:
		print(err)
