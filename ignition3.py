import requests
import json
import math
from time import sleep
from datetime import datetime

Voteaccount = "BVCaVh8mNzYgorruQJ7QvSg4PuggAfdbC71Qu5GNGRA8"

# Solana Ignition Hackathon East Asia 
# 3rXHdF7CfwG6K2VVFpvBRwdbRwyR5Zn7kQhLgxn4mjk7
# Solana Season Hackathon Asia 
# 437b1PsbmmW8Qi5KcNm8LTqsb4Q5ncvCTpyS3kPa5Yuh
# Solana Ignition Hackathon East Asia for Dorahacks
# BVCaVh8mNzYgorruQJ7QvSg4PuggAfdbC71Qu5GNGRA8

headers = {'Content-Type': 'application/json'}

url = 'https://api.mainnet-beta.solana.com'

pathtx = 'ignition_asia_tx.txt'
pathaddup = 'ignition_asia_addup.txt'

txfile = open(pathtx, 'w')
addupfile = open(pathaddup, 'w')

outarr = []


def arruni(listA):  # delet repeat things
	return sorted(set(listA), key=listA.index)

def voteoutput(list):  # address voted USDC add up function
    pass

def noneto0(num):
    try:
        num = int(num)
    except TypeError:
        num = 0
    return num


def countvoteusdc(votingreq,tx):
    if "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" in votingreq.text:  # If this tx voted USDC for Scallop
        voteresponsejson = json.loads(votingreq.text)
        voteraddress = voteresponsejson["result"]["transaction"]["message"]["accountKeys"][0]
        voterusdcbefore = noneto0(voteresponsejson["result"]["meta"]["preTokenBalances"][0]["uiTokenAmount"]["amount"]) # need to use "amount" * 1/1000000 cuz if using "uiAmount" it won't count decimals. 
        voterusdcafter = noneto0(voteresponsejson["result"]["meta"]["postTokenBalances"][0]["uiTokenAmount"]["amount"])
        voterusdc = voterusdcbefore - voterusdcafter
        outarr.append([[voteraddress, voterusdc],[tx]])
        txtout = voteraddress, voterusdc*math.pow(10, -6), tx
        print(txtout, file=txfile)
    # else:
    #     print(tx, "This tx is not a voting tx")


def voteoutput(outarr):

    output = []

    for addressandtx in outarr:
        output.append(addressandtx[0][0])

    output = arruni(output)

    # print(output)

    outputwithusdc = []
    for address in output:
        outputwithusdc.append([address, 0])

    # print(outputwithusdc)

    for addressandtx in outarr:
        for address in outputwithusdc:
            if address[0] == addressandtx[0][0]:
                address[1] += addressandtx[0][1]
    
    # print(outputwithusdc)

    for voteusdc in outputwithusdc:
        voteusdc[1] = voteusdc[1]*math.pow(10, -6)


    outputsort = sorted(outputwithusdc, key=lambda s: s[1], reverse=True)

    return outputsort

def main():

    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"), file=txfile)
    print(today.strftime("%Y-%m-%d %H:%M:%S"), file=addupfile)
    
    lastesttx = ""

    while True :

        if lastesttx == "":
            data = '{"jsonrpc":"2.0","id": 1, "method":"getSignaturesForAddress", "params":["' + Voteaccount + '",{"limit":1000}]}'
        else:
            # break
            data = '{"jsonrpc":"2.0","id": 1, "method":"getSignaturesForAddress", "params":["' + Voteaccount + '",{"limit":1000, "before":"'+ lastesttx +'"}]}'

        req = requests.post(url, headers=headers, data=data)
        reqjson = json.loads(req.text)

        try:
            lastesttx = reqjson["result"][len(reqjson["result"])-1]["signature"]
        except:
            print("We've hit the bottom of target datas!")
            break

        # print(lastesttx, "is the last tx")

        if len(reqjson["result"]) != 0:

            for i in range(0, len(reqjson["result"])):

                tx = reqjson["result"][i]["signature"]
            
                if reqjson["result"][i]["err"] == None:   # Only count success transaction.
                    data = '{"jsonrpc":"2.0","method":"getTransaction","id": 1,"params":["' + tx + '","json"]}'
                    datajson = json.loads(data)
                    datajson["params"][0] = tx
                    data = json.dumps(datajson)
                    votingreq = requests.post(url, headers=headers, data=data) # Send new req for details.
                    sleep(1)
                    # print(votingreq.text)

                    countvoteusdc(votingreq,tx)
        
        else:
            print("We've hit the bottom of target datas2!")
            break

    print("Scraping Over!")

    outputsort = voteoutput(outarr)
    for addressandvote in outputsort:
        print(addressandvote, file=addupfile)
    
    txfile.close()
    addupfile.close()


if __name__ == "__main__":
    main()
