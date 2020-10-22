import googlemaps
import json
import time
start_time = time.time()

import json
from collections import namedtuple
from json import JSONEncoder


import configparser#import the key from secret file
config = configparser.ConfigParser()
config.read("credentials.ini")#stored keys outside respository.
#google version getting name. Uses googlemaps module. and the key is kept secret
location = [44.644699, -123.305458]#for testing


def get_name_google(lat, long):

    gmaps = googlemaps.Client(key=config["DEFAULT"]["key_google"])#personal API key
    result = gmaps.reverse_geocode((lat, long))#gets json

    i = 0
    while i < len(result)-1:
        j = 0
        while j < len(result[i]["address_components"])-1:
            print(result[i]["address_components"][j])
            print()
            j+=1

        i+=1



# get_name_google(location[0], location[1])
