#!/usr/bin/python3

import re
from mathematicians import simple_get
from bs4 import BeautifulSoup

subie_dealer = {}

def main():
    print('Get subies!')
    get_used_subies('capital')
    print('len %d' % len(subie_dealer) )    

def save_site(site):
    open('page.txt', 'wb').write(site)
    
def get_used_subies(dealer):
    response = simple_get('https://www.capitolsubarusj.com/used-inventory/index.htm?compositeType=&year=&make=Subaru&model=Forester&trim=&bodyStyle=&driveLine=&internetPrice=&saveFacetState=true&lastFacetInteracted=inventory-listing1-facet-anchor-model-1')
     
    save_site(response)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = list()

        text_file = open("out.txt", "w")
        
        for li in html.select('li'):
            for name in li.text.split('\n'):
                if len(name) > 0:
                    if "Forester" in name:
                        names.append(name.strip())
                        print(">>>")
                        print(name)
                        print("<<<")
                        match = re.search(r"\d{4}",name)
                        if match:
                            print("year:",match.group(0))
                        text_file.write(">%s<\n" % name)

                    if "Engine" in name:
                        names.append(name.split(","))
                        text_file.write("***%s\n" % name)
                        print(name.split(","))

        return names

    raise Exception('Error retrieving contents at {}'.format(url))
 
if __name__ == '__main__':
    main()
    print('END GAME\n')
