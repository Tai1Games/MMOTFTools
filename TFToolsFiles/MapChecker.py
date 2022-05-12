import json
import io

def checkAll(filesFolder, keyNames):
    keyNames.print()
    fails = list()
    with io.open(filesFolder + '/mapejemplo.json', encoding='utf-8-sig') as json_data:
        roomsList = json.loads(json_data.read())
    
    for room in roomsList:
        for n in room['NodeConnections']:
            name = room['NodeConnections'][n]['ConnectingNode']

            if(keyNames.containsNode(name)):
                print(f'{name} Lo tenemos')
            else:
                print(f'{name} No lo tenemos')
