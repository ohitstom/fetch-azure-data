import json

def prettier(jsonObj):
    return json.dumps(jsonObj, indent=4, sort_keys=True)

def exportJson(jsonObj, filename):
    with open(f'data\\{filename}', 'w') as outfile:
        outfile.write(jsonObj)