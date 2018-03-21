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
        for dealer in subieDealerAddr:
            for car in subieDealer[dealer]:
                writer.writerow((car.salePrice, car.mileage,car.year,car.make,car.model,car.modelCode,car.stockNum,car.vin,car.extColor,car.intColor,car.transmission))

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

        for li in html.select('li'):
            text_file.write(">%s<\n" % li)
            for name in li.text.split('\n'):
                if len(name) > 0:
                    if "Forester" in name:
                        names.append(name.strip())
                        match = re.search(r"(\d{4})\s+(\w+)\s+(.+)*",name)
                        if match:
                            print("************************************************************")
                            carCount += 1
                            car_list.append(Car())
                            car_list[carCount - 1].year = match.group(1)
                            car_list[carCount - 1].make = match.group(2)
                            car_list[carCount - 1].model = match.group(3)
                            #print("\tyear:",match.group(1))
                            #print("\tmake:",match.group(2))
                            #print("\tremaining:",match.group(3))
                            #print(car_list[carCount - 1].year)
                            #print(car_list[carCount - 1].make)
                            #print(car_list[carCount - 1].model)
                            print("\tyear:%s" % car_list[carCount -1].year)
                            print("\tmake:%s" % car_list[carCount -1].make)
                            print("\tmodel:%s" % car_list[carCount -1].model)
                            
                    if "Now" in name:
                        match = re.search(r"(\d\d,\d\d\d)",name)
                        price = match.group(0).replace(',', '')
                        car_list[carCount - 1].salePrice = price
                        print("\tmatch:%s", name)
                        print("\tNow Price:%s" % car_list[carCount - 1].salePrice)
                        
                    if "Sale Price:" in name:
                        #if not any("Kelley" or "Retail" in name):
                            match = re.search(r"(\d\d,\d\d\d)",name)
                            price = match.group(0).replace(',', '')
                            car_list[carCount - 1].salePrice = price
                            print("\tSale Price:%s" % car_list[carCount - 1].salePrice)

                    if "Engine:" in name:
                        #print("New Car:%s\n" % name)
                        
                        names.append(name.split(","))
                        text_file.write("***%s\n" % name)

                        # Workaround to get mileage
                        if "Mileage" in name:
                            match = re.search(r"Mileage:\s(\d+,\d\d\d)", name)
                            if match:
                                mileage = match.group(1)
                                mileage = re.sub(',',"", mileage)
                                car_list[carCount - 1].mileage = mileage
                                print("\tMileage:%s" % car_list[carCount - 1].mileage) 
                        
                        attributes = name.split(",")

                        for item in attributes:
                            #print(item)
                            if "Transmission" in item:
                                match = re.search(r".+:\s(.+)", item)
                                if match:
                                    m = match.group(1)
                                    car_list[carCount - 1].transmission = match.group(1)
                                    #print(car_list[carCount - 1].transmission)
                                    print("\tTransmission:%s" % car_list[carCount - 1].transmission)
                            if "Exterior Color" in item:
                                match = re.search(r".+:\s(.+)", item)
                                if match:
                                    m = match.group(1)
                                    car_list[carCount - 1].extColor = match.group(1)
                                    print("\tExterior Color:%s" % car_list[carCount - 1].extColor)
                            if "Interior Color" in item:
                                match = re.search(r".+:\s(.+)", item)
                                if match:
                                    m = match.group(1)
                                    #print("\t%s" % m)
                                    car_list[carCount - 1].intColor = match.group(1)
                                    print("\tInterior Color:%s" % car_list[carCount - 1].intColor)
                            if "Stock #" in item:
                                match = re.search(r".+:[ ](\w+)", item)
                                if match:
                                    m = match.group(1)
                                    car_list[carCount - 1].stockNum = match.group(1)
                                    print("\tStock #:%s" % car_list[carCount - 1].stockNum)
                            if "Model Code" in item:
                                match = re.search(r".+:[ ](\w+)", item)
                                if match:
                                    m = match.group(1)
                                    car_list[carCount - 1].modelCode = match.group(1)
                                    print("\tModel Code:%s" % car_list[carCount - 1].modelCode)
                            if "VIN" in item:
                                match = re.search(r".+:[ ](\w{17})", item)
                                if match:
                                    m = match.group(1)
                                    car_list[carCount - 1].vin = match.group(1)
                                    print("\tVIN:%s" % car_list[carCount - 1].vin)
                    continue
                    print("************************************************************")

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
