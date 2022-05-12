import json
import io
from Error import ERRCODE
import Program

def checkConnectingNodes(roomsList, filePath, errorList, keyNames):
	for room in roomsList:
		for n in room['NodeConnections']:
			name = room['NodeConnections'][n]['ConnectingNode']

			if(keyNames.containsNode(name) != True):
				errorList.append((ERRCODE.NODE_DOES_NOT_EXISTS, filePath,
						  f"{name} node does not exists"))


def checkSingleEvent(event, filePath, errorList):
	requiredFields = Program.getEngineConstants(event['EventType'])
	for field in requiredFields:
		if(field not in event):
			errorList.append((ERRCODE.EVENT_MISSING_FIELD, filePath,
						f"{field} does not exist in event"))
		



def checkEventType(event, filePath, errorList):
	for e in event:
		if(Program.checkEngineConstant(e['EventType'], "EVENTTYPE") != True):
			errorList.append((ERRCODE.NODE_EVENT_DOES_NOT_EXIST, filePath,
						f"{e['EventType']} event does not exist"))
		else:
			checkSingleEvent(e, filePath, errorList)



def checkEvents(roomsList, filePath, errorList, keyNames):
	events = Program.getEngineConstants("EVENTS")
	
	for room in roomsList:
		for event in events:			 
			if(event in room):
				checkEventType(room[event], filePath, errorList)


def checkAll(filesFolder, keyNames):
	errorList = list()
	filePath = filesFolder + '/mapejemplo.json'
	with io.open(filePath, encoding='utf-8-sig') as json_data:
		roomsList = json.loads(json_data.read())
	

	checkConnectingNodes(roomsList, filePath, errorList, keyNames)
	checkEvents(roomsList, filePath, errorList, keyNames)



	for err in errorList:
		print(err)
