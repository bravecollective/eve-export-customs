import inspect
import os
import json

import ESI

newIDs = []

#If you've moved your static folder, set this variable to the path of the new folder (no trailing slash).
STATIC_PATH_OVERRIDE = None

def dataFile(extraFolder):

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.join(os.path.dirname(os.path.abspath(filename)))

    dataLocation = str(path) + extraFolder

    return(dataLocation)

staticPath = (STATIC_PATH_OVERRIDE) if (STATIC_PATH_OVERRIDE is not None) else (dataFile("/static"))

try:
    with open(staticPath + "/TypeIDs.json") as knownData:
        foundIDs = json.load(knownData)
        IDs = {int(key):foundIDs[key] for key in foundIDs}
except:
    IDs = {}

print("Checking for new IDs...")

counter = 1
max_page = 1

esi_handler = ESI.Handler()

while counter <= max_page:
    types_request = esi_handler.call("/universe/types/", page=counter, retries=2)

    if types_request["Success"]:

        max_page = int(types_request["Headers"]["X-Pages"])
        
        for eachID in types_request["Data"]:
            if int(eachID) not in IDs:
                newIDs.append(int(eachID))

        counter += 1
        
    else:
        
        raise Exception(
            "TYPES ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                data=types_request["Data"],
                headers=types_request["Headers"]
            )
        )

print("{found} new IDs found! Parsing names...".format(found=len(newIDs)))

pulls = [newIDs[x:x+1000] for x in range(0, len(newIDs), 1000)]

for eachPull in pulls:

    names_request = esi_handler.call("/universe/names/", items=eachPull, retries=2)

    if names_request["Success"]:

        for eachNew in names_request["Data"]:
            IDs[int(eachNew["id"])] = str(eachNew["name"])
        
    else:
        
        raise Exception(
            "NAMES ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                data=names_request["Data"],
                headers=names_request["Headers"]
            )
        )

print("Type ID List now contains {current} names!".format(current=len(IDs)))

with open(staticPath + "/TypeIDs.json", "w", encoding="utf-8", errors="replace") as writeFile:
    json.dump(dict(sorted(IDs.items())), writeFile, indent=1)

print("Json Export Successful...")
