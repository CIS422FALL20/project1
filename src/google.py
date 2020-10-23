import googlemaps
import json
import time
start_time = time.time()

import configparser#import the key from secret file
config = configparser.ConfigParser()
config.read("credentials.ini")#stored keys outside respository.
#google version getting name. Uses googlemaps module. and the key is kept secret
location = [44.848629,-123.237274]#for testing

#WORKING
class Address:
    def __init__(self, print_address, street):
        self.__print_address = print_address
        self.street = street

    #def __check_region(self, other):
    #    return self.zip == other.zip and  self.city == other.city and self.state == other.state and self.country == other.country

    def __eq__(self, other):
        return self.street == other.street

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.__print_address

def get_name_google(lat, long):
    gmaps = googlemaps.Client(key=config["DEFAULT"]["key_google"])#personal API key
    result = gmaps.reverse_geocode((lat, long))#gets json

    #address = None
    #for i in range(0, len(result)-1):
    #    for j in range(0, len(result[i]['address_components'])-1):
    #        #the Geometric_center is the tag that indicates the exact point, so we avoid problems with houses that are in front of 2 different streets.
    #        if result[i]['address_components'][j]['types'] == ['route']:
    #            street = result[i]
    #            address = Address()

    for component in result:
        if 'route' in component['types']: # and component['geometry']['location_type'] == 'GEOMETRIC_CENTER':
            for a in component['address_components']:
                if 'route' in a['types']:
                    full_address = component['formatted_address']
                    street = a["short_name"]
                    address = Address(full_address, street)
    return address
