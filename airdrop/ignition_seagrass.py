import json


def arruni(listA):  # delet repeat things
	return sorted(set(listA), key=listA.index)

def main():

    addarr = []
    outputwithusdc = []
    outputjson = []

    readjson = open('ignition_alltx_new.json', 'r')
    outjson = open('ignition_seagrass.json', 'w+')

    with readjson as f:
        listjson = json.load(f)

    for address in listjson:
        addarr.append(address['address'])

    addarr = arruni(addarr)

    for address in addarr:
        outputwithusdc.append([address, 0])
    
    # print(outputwithusdc)
    for address in outputwithusdc:
            for txlist in listjson:
                if address[0] == txlist['address']:
                    address[1] += float(txlist['VoteUSDC'])
    
    outputsort = sorted(outputwithusdc, key=lambda s: s[1], reverse=True) 

    for allvoter in outputsort:
        if allvoter[1] >= 2:
            addjson = {"authority": allvoter[0], "amount": 1}
            outputjson.append(addjson)

    outputjson = json.dumps(outputjson)

    print(outputjson, file=outjson)

if __name__ == "__main__":
    main()
