#!/usr/bin/python3

import re
import datetime
from mathematicians import simple_get
from bs4 import BeautifulSoup

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

subie_dealer = {}
subie_dealer['fremont'] = "https://www.premiersubaruoffremont.com/used-inventory/index.htm?make=Subaru&model=Forester&sortBy=internetPrice+asc&"
subie_dealer['capital'] = "https://www.capitolsubarusj.com/used-inventory/index.htm?make=Subaru&model=Forester&sortBy=internetPrice+asc&"

car_list = list()

def main():
    print('Get subies!')
    get_used_subies('capital')
    get_used_subies('fremont')
    print('Dealer Count %d' % len(subie_dealer) )    

def save_site(site):
    open('page.txt', 'wb').write(site)
    
def get_used_subies(dealer):
    #response = simple_get('https://www.capitolsubarusj.com/used-inventory/index.htm?compositeType=&year=&make=Subaru&model=Forester&trim=&bodyStyle=&driveLine=&internetPrice=&saveFacetState=true&lastFacetInteracted=inventory-listing1-facet-anchor-model-1')
    response = simple_get(subie_dealer[dealer])
     
    save_site(response)
    
    carCount = 0

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = list()

        text_file = open("out.txt", "w")
        
        for li in html.select('li'):
            text_file.write(">%s<\n" % li)
            for name in li.text.split('\n'):
                if len(name) > 0:
                    if "Now" in name:
                        match = re.search(r"(\d\d,\d\d\d)",name)
                        price = match.group(0).replace(',', '')
                        car_list[carCount - 1].salePrice = price
                        print("\tNow Price:%s" % car_list[carCount - 1].salePrice)
                        
                    if "Price:" in name:
                        if "Kelley" not in name:
                            print("Sale Price: %s" % name)

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
                                #car_list[carCount - 1].extColor = match.group(1)
                                print("\tMileage:%s" % mileage)
                        
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
        return names

    raise Exception('Error retrieving contents at {}'.format(url))
 
if __name__ == '__main__':
    main()
    print('END GAME\n')
