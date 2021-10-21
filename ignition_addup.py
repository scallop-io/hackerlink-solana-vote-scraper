import json
import requests
import math
from time import sleep
from datetime import datetime

def main():

    newtxt = open('ignition_asia_tx_new.txt', 'r')
    oldtxt = open('ignition_asia_tx.txt', 'r')
    adduptxt = open('ignition_addup_new.txt', 'w+')

    oldtext = oldtxt.read()

    newtext = newtxt.read()

    addup = newtext + oldtext

    print(addup, file=adduptxt)


    newtxt.close()
    oldtxt.close()
    adduptxt.close()


if __name__ == "__main__":
    main()
