import re
import json

backuppath = open('ignition_addup_new.txt', 'r')
backupjson = open('ignition_list.json', 'w')

def usdcfilter(str):
    str = re.sub(r"\s+", "", str)
    str = re.sub(r",", "", str)
    str = str.replace(" ", "")
    return str


listtext = backuppath.read()

result = re.split('[\']', listtext)

outjson = []

for i in range(1, len(result), 4):

    data = {}       
    data["address"] = result[i]
    data["VoteUSDC"] = usdcfilter(result[i+1])
    data["signature"] = result[i+2]
    outjson.append(data)


output = json.dumps(outjson)
backupjson.write(output)


backuppath.close()
backupjson.close()

print("Converted!")




