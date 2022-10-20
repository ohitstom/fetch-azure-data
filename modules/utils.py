import json
import os 

def prettier(jsonObj):
    return json.dumps(jsonObj, indent=4, sort_keys=True)

def exportJson(jsonObj, filename):
    if not os.path.isdir("data"):
        os.mkdir("data")
    with open(f'data\\{filename}', 'w') as outfile:
        outfile.write(jsonObj)