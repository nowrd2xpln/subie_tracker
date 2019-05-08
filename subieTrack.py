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
dealershipFile = "./ds_short.txt"
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

    dump_cars_to_csv()

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
        html_str = str(html)

        names = list()

        text_file = open("out.txt", "w")
        
        print("DEALER: %s" % dealer.name)

        print("DBGDBG\n")
        dbgtest = html.findAll("div", attrs={'data-widget-name':'tracking-ddc-data-layer'})
        dbgtest_str = str(dbgtest)
       #print("\t%s\n" % dbgtest)
        print("DBGDBG\n")

        stuff = []
        test_list = []
        datalayer = []
        cnt = 0
        db = {}

        print(type(dbgtest_str))

        # Get Vehicle datalayer
        match = re.search(r"DDC.dataLayer\['(\w+)'\]\s+=\s+\[\n?(.*\n)+\];",dbgtest_str, re.UNICODE)
        mat_tup = ""
        if match:
            print("************************************************************")
            test_list = match.group(0)
            #print(test_list)
            #mat_tup = re.search(r"\{\n(.*\n)+(\}\n)",test_list, re.UNICODE)
            #mat_tup = re.findall(r"\{\n(.*,?\n)+(\}\n)",test_list, re.UNICODE)

            # Grab each car
            mat_tup = re.findall(r"\{\n((\".*\n)+\})",test_list, re.UNICODE)
            if mat_tup:
                print("cars:%d\n" % (len(mat_tup)))
                print(*mat_tup, sep = "\n\n")
            
            print("************************************************************")

        # for item in dbgtest:
        #     cnt += 1
        #     #print("%02d:%s\n" % (cnt, item))
        #     stuff.append(item)
        #     print(cnt)
        #     print("%02d:%s\n" % (cnt-1, stuff[cnt-1]))

        
        print("Car Count %d" % carCount)
        print(len(car_list))

        # Add carlist to 
        #subieDealer[dealer] = list(car_list)
        #subieDealer[dealer] = list(car_list)
        #subieDealer[dealer] = car_list[:]
        dealer.carlist = car_list[:]
        del car_list[:]

        return names

    raise Exception('Error retrieving contents at {}'.format(url))
 
if __name__ == '__main__':
    main()
    print('END GAME\n')
