#!/usr/bin/python3

import re
import datetime
import time
import csv
import copy
from mathematicians import simple_get
from bs4 import BeautifulSoup
from time import gmtime, strftime

class Dealer(object):
    def __init__(self):
        location = ""
        name = ""
        url = ""
        carlist = []

class Car:
    make = ""
    model = ""
    modelCode = ""
    year = 0
    stockNum = ""
    vin = ""
    extColor = ""
    intColor = ""
    transmission = ""
    salePrice = ""
    mileage = 0

subieDealerAddr = {}
subieDealerAddr['fremont'] = "https://www.premiersubaruoffremont.com/used-inventory/index.htm?make=Subaru&model=Forester&sortBy=internetPrice+asc&"
subieDealerAddr['capital'] = "https://www.capitolsubarusj.com/used-inventory/index.htm?make=Subaru&model=Forester&sortBy=internetPrice+asc&"
dealershipFile = "./dealerships.txt"
subieDealer = {}

dealer_list = []
car_list = list()

def main():
    print('Get subies!')
#    get_used_subies('fremont')
#    get_used_subies('capital')
#   print('Dealer Count %d' % len(subieDealerAddr) )    
    
#    get_all_forester_list()
#    dump_cars_to_csv()

    # Get Dealership list from file
    get_dealership_list()

    # Get Forester list from dealerships
    for d in dealer_list:
        get_used_subies(d)
        break
#    dump_cars_to_csv()

    print("ENDGAME")
 
def get_dealership_list():
    fh = open(dealershipFile)
    
    dealershipList = fh.readlines()
    dealer = Dealer() 
    for line in dealershipList:
        dealerItems = line.split(",")
        dealer.location = dealerItems[0]
        dealer.name = dealerItems[1]
        dealer.url = dealerItems[2]
        dealer_list.append(copy.deepcopy(dealer))
        
    print("dealer_list %d" % len(dealer_list))

    for d in dealer_list:
        print("%s\n\t%s\n\t%s" % (d.location, d.name, d.url))

def save_site(site):
    open('page.txt', 'wb').write(site)
   
def get_all_forester_list():
    print("Get all forester list")

    counter = 0
    for dealer in subieDealerAddr:
        cnt = len(subieDealer[dealer])
        print("%s: %d" % (dealer, cnt))
        for car in subieDealer[dealer]:
            counter += 1
            print("%d" % counter)
            print("\tPrice:         %s" % car.salePrice)
            print("\tMileage:       %s" % car.mileage)
            print("\tMake:          %s" % car.make)
            print("\tModel:         %s" % car.model)
            print("\tModelCode:     %s" % car.modelCode)
            print("\tYear:          %s" % car.year)
            print("\tStockNumber:   %s" % car.stockNum)
            print("\tVIN:           %s" % car.vin)
            print("\tExteriorColor: %s" % car.extColor)
            print("\tInteriorColor: %s" % car.intColor)
            print("\tTransmission:  %s" % car.transmission)
        counter = 0
    
def dump_cars_to_csv():
    fname = './'
    fname += time.strftime("%Y%m%d")
    fname += '.csv'

    with open(fname, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        #for dealer in subieDealerAddr:
        #    for car in subieDealer[dealer]:
        #        writer.writerow((car.salePrice, car.mileage,car.year,car.make,car.model,car.modelCode,car.stockNum,car.vin,car.extColor,car.intColor,car.transmission))
        writer.writerow(("Location","Name","Sale Price", "Mileage","Year","Make","Model","Model Code","Stock Number","VIN","Exterior Color","Interior Color","Transmission"))
        for d in dealer_list:
            for car in d.carlist:
                writer.writerow((d.location,d.name,car.salePrice, car.mileage,car.year,car.make,car.model,car.modelCode,car.stockNum,car.vin,car.extColor,car.intColor,car.transmission))

def get_used_subies(dealer):
    #response = simple_get('https://www.capitolsubarusj.com/used-inventory/index.htm?compositeType=&year=&make=Subaru&model=Forester&trim=&bodyStyle=&driveLine=&internetPrice=&saveFacetState=true&lastFacetInteracted=inventory-listing1-facet-anchor-model-1')
    #response = simple_get(subieDealerAddr[dealer])
    response = simple_get(dealer.url)
     
    save_site(response)
    
    carCount = 0

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = list()

        text_file = open("out.txt", "w")
        
        print("DEALER: %s" % dealer.name)

        
        # pat = 'DDC.dataLayer\[\'vehicles\'\]'
        for tag in html.select('script'):
            #text_file.write(">%s<\n" % li)
            if tag.text.find('function(DDC)') != -1:
                print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                print (tag.text)
                print ("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
 
if __name__ == '__main__':
    main()
    print('END GAME\n')
