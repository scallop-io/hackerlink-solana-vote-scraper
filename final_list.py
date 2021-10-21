import json
from datetime import datetime


def arruni(listA):  # delet repeat things
	return sorted(set(listA), key=listA.index)

def main():

    today = datetime.now()

    addarr = []

    readjsonlist = open('ignition_list.json', 'r')
    adduptxt = open('ignition_addup_final.txt', 'w+')

    with readjsonlist as f:
        listjson = json.load(f)
    


    for address in range(0, len(listjson)):
        addarr.append(listjson[address]['address'])

    addarr = arruni(addarr)

    outputwithusdc = []

    for address in addarr:
        outputwithusdc.append([address, 0])
    
    # print(outputwithusdc)
    for address in outputwithusdc:
            for txlist in listjson:
                if address[0] == txlist['address']:
                    address[1] += float(txlist['VoteUSDC'])
    
    outputsort = sorted(outputwithusdc, key=lambda s: s[1], reverse=True)

    print(today.strftime("%Y-%m-%d %H:%M:%S"), file=adduptxt)
    print("Voted address:", len(listjson), file=adduptxt)


    addupusdc = 0
    for usdcarr in outputsort:
        addupusdc += usdcarr[1]
    print("Add up USDC:", addupusdc, file=adduptxt)

    for i in outputsort:
        print(i, file=adduptxt)


if __name__ == "__main__":
    main()
