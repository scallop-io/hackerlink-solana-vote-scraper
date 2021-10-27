import json
import requests
import math
from time import sleep
from datetime import datetime

def main():

    oldtxjson = open('ignition_list.json', 'r')
    newtxjson = open('ignition_list_new.json', 'r')
    addupjson = open('ignition_alltx_new.json', 'w+')

    with oldtxjson as f:
        oldlistjson = json.load(f)

    with newtxjson as f:
        newlistjson = json.load(f)

    adduplistjson=[]

    for newtx in newlistjson:
        adduplistjson.append(newtx)
    
    for oldtx in oldlistjson:
        adduplistjson.append(oldtx)
   

    newliststr = json.dumps(adduplistjson)

    addupjson.write(newliststr)

    print("Add up over!")

    oldtxjson.close()
    newtxjson.close()
    addupjson.close()


if __name__ == "__main__":
    main()
