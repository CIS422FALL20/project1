#FINDS THE TURNING POINTS, IT RETURNS THE NAMES AND THE NUMBER OF THE INDEX WHERE THE TURNS ARE.
#it gets the info  from the points from the gpx files and perform a recursion search
#to get the points where the streets changes. used the module "google" from where it connects to google
#maps and get the name of the address where some point (lat,long) is located.
#returns and 2d Array witht [gpx index number, name of streets, latitude, longitud]
#latest version (10/20/20)
import googlemaps
import json
from google import get_name_google
from getgpx import *
import gpxpy
import math
from math import cos, sin, asin, radians, sqrt
#import Cartographics


# from distance import distance
from multiprocessing.pool import ThreadPool#multi process
# import gpxpy
# import time
# import threading
#
# from multiprocessing import Process#to run concurrently.


class Route:

    def __init__(self, list):
        self.__arr = [] # lat / lon The points, from the gpx live here.
        for i in list:
            self.__arr.append(i)
        self.__pool = [None]*len(list) # street name, cache to reduce the number of requests, collisions will prevent requesting more data.
        self.__storage = [] # address and index

    def add_point(self, index):#for the one and last point:
        self.__storage.append([index, get_name_google(self.__arr[index].get_lat(), self.__arr[index].get_long()), self.__arr[index].get_lat(), self.__arr[index].get_long()])

    #adding starting point of the whole road
    # intersection.append([start, get_name_google(list[start].get_lat(), list[start].get_long()), list[start].get_lat(), list[start].get_long()])
    def change(self):
        self.__r_change(0, len(self.__arr)-1)
        #self.__storage.extend(Cartographics.find_direction_points(self.__arr))
        print("DONE")


    #calling fuction, returns one list of array, "intersectation" is an array that contains the results.
    # change(start, end, intersection)
    #adding ending point
    # intersection.append([end, get_name_google(list[end].get_lat(), list[end].get_long()), list[end].get_lat(), list[end].get_long()]

    def direction(self,input):#array of indexes

        result = []
        turn = ""
        rango = 20
        result.append([])
        for i in range(0,len(input)-1):
            degree = 0
            if i == 0:
                degree = 180
            else:
                a = [self.__arr[input[i]-rango].get_lat(), self.__arr[input[i]-rango].get_long()]
                b = [self.__arr[input[i]].get_lat(), self.__arr[input[i]].get_long()]
                c = [self.__arr[input[i]+rango].get_lat(), self.__arr[input[i]+rango].get_long()]
                degree = self.get_angle(a,b,c)

            if degree < 130 or degree > 240 or i == 0:
                # print(route_distance(input[i], input[i+1]))
                # print("{}: {},{} = {}".format(degree, position[input[i]].get_lat(), position[input[i]].get_long(),get_name_google(position[input[i]].get_lat(),position[input[i]].get_long())))
                if degree > 240:
                    turn = "Right"
                    # print("right")
                if degree < 130:
                    turn = "Left"
                    # print("left")

                meters = self.route_distance(input[i], input[i+1])

                result.append([input[i], turn, meters, get_name_google( self.__arr[input[i]].get_lat(), self.__arr[input[i]].get_long()), self.__arr[input[i]].get_lat(), self.__arr[input[i]].get_long() ])

        return result

    def route_distance(self,start, end):
        #return Cartographics.route_distance(self.__arr, start, end)
        segment = 0
        for i in range(start,end):
            segment+=self.distance(self.__arr [i].get_lat(), self.__arr [i].get_long(), self.__arr [i+1].get_lat(), self.__arr [i+1].get_long())
        return segment

    def get_angle(self,a, b, c):

        ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        return ang + 360 if ang < 0 else ang

    def distance(self,ini_lat, ini_lon, fin_lat, fin_lon):
        #return Cartographics.route_distance((ini_lat, ini_lon), (fin_lat, fin_lon))
        dif_lat = radians(ini_lat) - radians(fin_lat)
        dif_lon = radians(ini_lon) - radians(fin_lon)
        earth_radio = 6371 #radius in km
        distance = (sin(dif_lat/2))**2 + cos(radians(ini_lat)) * cos(radians(fin_lat)) * (sin(dif_lon/2))**2
        distancia = earth_radio * asin(sqrt(distance)) * 2 * 1000 # multiply by 1000 to convert to 	distance in meters
        return distancia

    def result(self):
        self.add_point(0)
        end = len(self.__arr)-2
        self.change()
        self.add_point(end+1)
        self.__storage.sort(key=lambda x: x[0])#sort order

        # print(self.__storage)
        index = []
        for elem in self.__storage:
            try:
                index.append(elem[0])
            except:
                pass

        final = self.direction(index)

        return final

    def __r_change(self, start, end):#list contains all the points, start first point, end last one and storage saves the results.
        middle = int((start+end)/2)

        #parts1 = [[0,start],[1,middle],[2,end]]
        #self.request(parts1)

        p_start = get_name_google(self.__arr[start].get_lat(), self.__arr[start].get_long())
        p_mid = get_name_google(self.__arr[middle].get_lat(), self.__arr[middle].get_long())
        p_end = get_name_google(self.__arr[end].get_lat(), self.__arr[end].get_long())

        #p_mid1 = get_name_google(self.__arr[middle - 1].get_lat(), self.__arr[middle - 1].get_long())
        #p_mid2 = get_name_google(self.__arr[middle + 1].get_lat(), self.__arr[middle + 1].get_long())

        # base case: when  the start, the middle and the end is the same.
        if p_start == p_mid and p_mid == p_end:
            #print("reached end//")
            return
        # when start and middle are equal and middle and end not equal(or viceverse), possible indication of a point of change.
        if (p_start == p_mid and p_mid != p_end) or (p_start != p_mid and p_mid == p_end):

            #parts2 = [[0,middle+1], [1,middle-1]]
            #self.request(parts2)
            p_mid1 = get_name_google(self.__arr[middle - 1].get_lat(), self.__arr[middle - 1].get_long())
            p_mid2 = get_name_google(self.__arr[middle + 1].get_lat(), self.__arr[middle + 1].get_long())

            #checks if the next point from the middle is different, if it is, change detected and added.
            if p_mid != p_mid1:
                self.__storage.append([middle-1, p_mid1, self.__arr[middle-1].get_lat(), self.__arr[middle-1].get_long()])
            elif p_mid != p_mid2:
                self.__storage.append([middle, p_mid2, self.__arr[middle].get_lat(), self.__arr[middle].get_long()])
            else:
                self.__r_change(start, middle)
                self.__r_change(middle+1, end)
        else:
            p_mid1 = get_name_google(self.__arr[middle - 1].get_lat(), self.__arr[middle - 1].get_long())
            p_mid2 = get_name_google(self.__arr[middle + 1].get_lat(), self.__arr[middle + 1].get_long())

            # checks if the next point from the middle is different, if it is, change detected and added.
            if p_mid != p_mid1:
                self.__storage.append([middle, p_mid, self.__arr[middle].get_lat(), self.__arr[middle].get_long()])
            if p_mid != p_mid2:
                self.__storage.append([middle + 1, p_mid2, self.__arr[middle + 1].get_lat(), self.__arr[middle + 1].get_long()])
            self.__r_change(start, middle)
            self.__r_change(middle+1, end)
