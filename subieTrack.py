#!/usr/bin/python3

import re
from mathematicians import simple_get
from bs4 import BeautifulSoup

class Car:
    make = ""
    model = ""
    year = 0
    stockNum = ""
    vin = ""
    extColor = ""
    intColor = ""
    transmission = ""
    salePrice = float(0)

subie_dealer = {}

def main():
    print('Get subies!')
    get_used_subies('capital')
    print('Dealer Count %d' % len(subie_dealer) )    

def save_site(site):
    open('page.txt', 'wb').write(site)
    
def get_used_subies(dealer):
    response = simple_get('https://www.capitolsubarusj.com/used-inventory/index.htm?compositeType=&year=&make=Subaru&model=Forester&trim=&bodyStyle=&driveLine=&internetPrice=&saveFacetState=true&lastFacetInteracted=inventory-listing1-facet-anchor-model-1')
     
    save_site(response)
    
    carCount = 0

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = list()

        text_file = open("out.txt", "w")
        
        for li in html.select('li'):
            for name in li.text.split('\n'):
                if len(name) > 0:
                    if "Forester" in name:
                        names.append(name.strip())
                        match = re.search(r"(\d{4})\s+(\w+)\s+(.+)*",name)
                        if match:
                            print("************************************************************")
                            print("\tyear:",match.group(1))
                            print("\tmodel:",match.group(2))
                            print("\tremaining:",match.group(3))
                            
                        text_file.write(">%s<\n" % name)

                    if "Engine:" in name:
                        #print("New Car:%s\n" % name)
                        carCount += 1
                        
                        names.append(name.split(","))
                        text_file.write("***%s\n" % name)
                        attributes = name.split(",")
                        for item in attributes:
                            if "Transmission" in item:
                                #print(item)
                                match = re.search(r".+:[ ](\w+)", item)
                                if match:
                                    m = match.group(1)
                                    print("\t%s" % m)
                            if "Exterior Color" in item:
                                #print(item)
                                match = re.search(r".+:[ ](\w+)", item)
                                if match:
                                    m = match.group(1)
                                    print("\t%s" % m)
                            if "Interior Color" in item:
                                #print(item)
                                match = re.search(r".+:[ ](\w+)", item)
                                if match:
                                    m = match.group(1)
                                    print("\t%s" % m)
                            if "Stock #" in item:
                                #print(item)
                                match = re.search(r".+:[ ](\w+)", item)
                                if match:
                                    m = match.group(1)
                                    print("\t%s" % m)
                            if "Model Code" in item:
                                #print(item)
                                match = re.search(r".+:[ ](\w+)", item)
                                if match:
                                    m = match.group(1)
                                    print("\t%s" % m)
                            if "VIN" in item:
                                #print(item)
                                match = re.search(r".+:[ ](\w+)", item)
                                if match:
                                    m = match.group(1)
                                    print("\t%s" % m)
                    continue
                    print("************************************************************")

        print("Car Count %d" % carCount)
        return names

    raise Exception('Error retrieving contents at {}'.format(url))
 
if __name__ == '__main__':
    main()
    print('END GAME\n')
