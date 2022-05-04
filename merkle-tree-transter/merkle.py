from functools import reduce
import numpy
import json


def main():

    riptide_array = numpy.load('../riptide_array.npy')

    merkle_seagrass_json = []
    merkle_riptide_json = []
    merkle_fossil_json = []

    merkle_double_arr =[]   
    merkle_moray_json = []

    for tx in riptide_array:     

        data = {}
        data["authority"] = tx[0]
        data["amount"] = 1
        merkle_seagrass_json.append(data)

    with open("seagrass.json", "w+") as MorayJson:
        data = merkle_seagrass_json
        json.dump(data, MorayJson)


    for tx in riptide_array:
        if float(tx[1]) >= 3:
            data = {}
            data["authority"] = tx[0]
            data["amount"] = 1
            merkle_riptide_json.append(data)

    FossilList = open('.\Fossil-2022-05-02.txt', 'r')
    FossilAddressArr = FossilList.readlines()

    FossilAddressArrStrip = []

    for address in FossilAddressArr:
       FossilAddressArrStrip.append(address.rstrip())

    for address in FossilAddressArrStrip:
            data = {}
            data["authority"] = address
            data["amount"] = 1
            merkle_fossil_json.append(data)
        
    with open("moray_riptide.json", "w+") as MorayJson:
        data = merkle_riptide_json
        json.dump(data, MorayJson)
    
    with open("moray_fossil.json", "w+") as MorayJson:
        data = merkle_fossil_json
        json.dump(data, MorayJson)

    for RiptideAddress in merkle_riptide_json:
        # print(RiptideAddress['authority'])
        if RiptideAddress in merkle_fossil_json:
            RiptideAddress['amount'] += 1
            merkle_double_arr.append(RiptideAddress['authority'])
            # print(RiptideAddress)

    for FossilAddress in merkle_fossil_json:
        if FossilAddress['authority'] not in merkle_double_arr:
            merkle_riptide_json.append(FossilAddress)
    
    print(merkle_riptide_json)

    with open("moray.json", "w+") as MorayJson:
        data = merkle_riptide_json
        json.dump(data, MorayJson)

    FossilList.close()


if __name__ == "__main__":
    main()
