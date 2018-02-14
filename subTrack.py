#!/usr/bin/python3

from mathematicians import simple_get
from bs4 import BeautifulSoup

subie_dealer = {}

def main():
    print('Get subies!')
    get_used_subies('capital')
    print('len %d' % len(subie_dealer) )    

def get_used_subies(dealer):
    response = simple_get('https://www.capitolsubarusj.com/used-inventory/index.htm?compositeType=&year=&make=Subaru&model=Forester&trim=&bodyStyle=&driveLine=&internetPrice=&saveFacetState=true&lastFacetInteracted=inventory-listing1-facet-anchor-model-1')
     
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        names = list()

        text_file = open("out.txt", "w")
        
        for li in html.select('li'):
            for name in li.text.split('\n'):
                if len(name) > 0:
                    names.append(name.strip())
                #print(name)
                    text_file.write(">%s<\n" % name);

        return names

    raise Exception('Error retrieving contents at {}'.format(url))
 
if __name__ == '__main__':
    main()
    print('END GAME\n')
