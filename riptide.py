import json
import math
from time import sleep
from datetime import datetime
from solana.rpc.api import Client
import asyncio

Voteaccount = "GhJVN91EJ7M68dXDVWoJvNbr5Gsqyb2wyoo8p5G6rRxL"  # Scallop voting PDA

pathtx = 'riptide_asia_tx.txt'
pathaddup = 'riptide_asia_addup.txt'

txfile = open(pathtx, 'w')
addupfile = open(pathaddup, 'w')
outarr = []

def arruni(listA):  # delet repeat things
	return sorted(set(listA), key=listA.index)


def noneto0(num):
    try:
        num = int(num)
    except TypeError:
        num = 0
    return num


def outputjson(outarr):
    backupjson = open('riptide_list.json', 'w+')
    outjson = []
    for tx in outarr:
        data = {}
        data["address"] = tx[0][0]
        data["VoteUSDC"] = tx[0][1]*math.pow(10, -6)
        data["signature"] = tx[1]
        outjson.append(data)
    output = json.dumps(outjson)
    backupjson.write(output)
    backupjson.close()


def voteoutput(outarr):  # address voted USDC add up function

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


def addupout(outarr):
    addupusdc = 0
    for addusd in outarr:
        addupusdc += addusd[0][1]
    print("Add up USDC:", addupusdc*math.pow(10, -6), file=txfile)

async def main():

    solana_client = Client("https://api.mainnet-beta.solana.com") # Don't use Serum RPC

    today = datetime.now()
    print(today.strftime("%Y-%m-%d %H:%M:%S"), file=txfile)
    print(today.strftime("%Y-%m-%d %H:%M:%S"), file=addupfile)

    lastesttx = ""

    while True:

        if lastesttx == "":

            reqjson = solana_client.get_confirmed_signature_for_address2(Voteaccount, limit=1000)

        else:
            # break
            reqjson = solana_client.get_confirmed_signature_for_address2(Voteaccount, before=lastesttx)

        resultlen = len(reqjson["result"])

        try:
            lastesttx = reqjson["result"][resultlen-1]["signature"]

        except:
                print("We've hit the bottom of target datas!")
                break

        if len(reqjson["result"]) != 0:

            print(len(reqjson["result"]))

            for i in range(0, len(reqjson["result"])):

                tx = reqjson["result"][i]["signature"]

                # Only count success transaction.
                if reqjson["result"][i]["err"] == None:

                    print(tx)

                    votingreqjson = solana_client.get_confirmed_transaction(tx)

                    sleep(1)

                    if "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" in json.dumps(votingreqjson):  # If this tx voted USDC for Your Project (This should be upgrade!!!)

                        voteraddress = votingreqjson["result"]["transaction"]["message"]["accountKeys"][0]

                        try:

                            preBalances = noneto0(votingreqjson["result"]["meta"]["preTokenBalances"][0]["uiTokenAmount"]["amount"])
                            postBalances = noneto0(votingreqjson["result"]["meta"]["postTokenBalances"][0]["uiTokenAmount"]["amount"])

                        except:

                            print("Captching amount error, Maybe we've hit the bottom.")
                            break

                        voterusdc = abs(preBalances - postBalances) #sometimes the order is not correct. so we need to abs().

                        # print(voterusdc)

                        outarr.append([[voteraddress, voterusdc], [tx]])

                        txtout = voteraddress, voterusdc*math.pow(10, -6), tx
                        print(txtout, file=txfile)

        else:
            break

    outputjson(outarr)

    addupout(outarr)

    print("Scraping Over!")

    outputsort = voteoutput(outarr)
    for addressandvote in outputsort:
        print(addressandvote, file=addupfile)

    txfile.close()
    addupfile.close()


asyncio.run(main())
