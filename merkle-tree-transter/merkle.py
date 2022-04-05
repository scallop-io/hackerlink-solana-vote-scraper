import numpy
import json


def main():

    riptide_array = numpy.load('../riptide_array.npy')

    merkle_seagrass_json = []
    merkle_moray_json = []

    for tx in riptide_array:     

        data = {}
        data["authority"] = tx[0]
        data["amount"] = 1
        merkle_seagrass_json.append(data)

    print(merkle_seagrass_json)

    for tx in riptide_array:
        if float(tx[1]) >= 3:
            data = {}
            data["authority"] = tx[0]
            data["amount"] = 1
            merkle_moray_json.append(data)

    print(merkle_moray_json)


    # merklejson = open('merkle_list.json', 'w+')


if __name__ == "__main__":
    main()
