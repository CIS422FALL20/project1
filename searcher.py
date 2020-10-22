#FINDS THE TURNING POINTS, IT RETURNS THE NAMES AND THE NUMBER OF THE INDEX WHERE THE TURNS ARE.
#it gets the info  from the points from the gpx files and perform a recursion search
#to get the points where the streets changes. used the module "google" from where it connects to google
#maps and get the name of the address where some point (lat,long) is located.
#returns and 2d Array witht [gpx index number, name of streets, latitude, longitud]
#latest version (10/20/20)
from google import get_name_google
from getgpx import *
import gpxpy
import math

# from distance import distance
from multiprocessing.pool import ThreadPool#multi process
# import gpxpy
# import time
# import threading
#
# from multiprocessing import Process#to run concurrently.

# start_time = time.time()#record time
#get the points from the gpx file
# file = open('09_27_20.gpx', 'r')#for testing, it won't be here for final version
# parseado = gpxpy.parse(file)
# list = get_points(parseado) #array of objects that hold information like lat, long, elev, time.

#first point and last one that are in the range is verify
# start = 0#first point
# end = len(list)-1#last point
# print("Start: {} End:{}".format(start,end))#debug

class Route:

    def __init__(self, list, size):
        self.__arr = []#The points from the gpx live here.
        for i in list:
            self.__arr.append(i)
        self.__pool = [""]*len(list)#cache to reduce the number of requests, collisions will prevent requesting more data.
        self.__storage = []

    def request(self,parts):#extract points, get the name address and add the info into the pool array(cache)

        thpool = ThreadPool(processes=1)
        interpolate = [""]*3

        for i in parts:
            if self.__pool[i[1]] == "":#if the data is in the cache array, it will not request the data but use the one from the pool array
                async_result = thpool.apply_async(get_name_google,(self.__arr[i[1]].get_lat(), self.__arr[i[1]].get_long()))
                interpolate[i[0]] = async_result.get()#holds more than one request.
                self.__pool[i[1]] = interpolate[i[0]]

    def add_point(self, index):#for the one and last point:
        print("entro")
        self.__storage.append([index, get_name_google(self.__arr[index].get_lat(), self.__arr[index].get_long()), self.__arr[index].get_lat(), self.__arr[index].get_long()])

    #adding starting point of the whole road
    # intersection.append([start, get_name_google(list[start].get_lat(), list[start].get_long()), list[start].get_lat(), list[start].get_long()])
    def change(self, start, end):#list contains all the points, start first point, end last one and storage saves the results.
        middle = int((start+end)/2)

        parts1 = [[0,start],[1,middle],[2,end]]
        self.request(parts1)

        # base case: when  the start, the middle and the end is the same.
        if self.__pool[start] == self.__pool[middle] and self.__pool[middle] == self.__pool[end]:
            return

        # when start and middle are equal and middle and end not equal(or viceverse), possible indication of a point of change.
        if (self.__pool[start] == self.__pool[middle] and  self.__pool[middle] != self.__pool[end]) or (self.__pool[start] != self.__pool[middle] and  self.__pool[middle] == self.__pool[end]):

            parts2 = [[0,middle+1], [1,middle-1]]
            self.request(parts2)

            #checks if the next point from the middle is different, if it is, change detected and added.
            if  self.__pool[middle-1] != self.__pool[middle]:
                self.__storage.append([middle-1, self.__pool[middle-1], self.__arr[middle-1].get_lat(), self.__arr[middle-1].get_long()])
            elif self.__pool[middle] != self.__pool[middle+1]:
                self.__storage.append([middle, self.__pool[middle], self.__arr[middle].get_lat(), self.__arr[middle].get_long()])
            else:
                self.change(start, middle)
                self.change(middle+1, end)

        else:
            parts3 = [[0,middle+1], [1,middle-1]]
            self.request(parts3)
            #checks when start, middle and end are different but the middle falls exactly in a changing point. it will perform the checking and add the point if it falls in the changing point.
            if self.__pool[middle-1] != self.__pool[middle]:
                self.__storage.append([middle-1, self.__pool[middle-1], self.__arr[middle-1].get_lat(), self.__arr[middle-1].get_long()])
            elif self.__pool[middle] != self.__pool[middle+1]:
                self.__storage.append([middle, self.__pool[middle], self.__arr[middle].get_lat(), self.__arr[middle].get_long()])
            #will continue dividing and searching.
            self.change(start, middle)
            self.change(middle+1, end)

#calling fuction, returns one list of array, "intersectation" is an array that contains the results.
# change(start, end, intersection)
#adding ending point
    # intersection.append([end, get_name_google(list[end].get_lat(), list[end].get_long()), list[end].get_lat(), list[end].get_long()]
    def get_angle(before, center, after):
        ang = math.degrees(math.atan2(after[1]-center[1], after[0]-after[0]) - math.atan2(before[1]-center[1], before[0]-center[0]))
        result = ang + 360 if ang < 0 else ang
        return result

    def route_distance(start, end):
        segment = 0
        for i in range(start, end):
            segment+=distance(self.__arr[i].get_lat(), self.__arr[i].get_long(), self.__arr[i+1].get_lat(), self.__arr[i+1].get_long())
        return segment

    def detect_turn():
        for i in range(1,len(list)-1):
            degres = getAngle((position[self.__arr[i]-rango].get_lat(),position[self.__arr[i]-rango].get_long()), (position[self.__arr[i]].get_lat(),position[list[i]].get_long()), ( position[self.__arr[i]+rango].get_lat(),position[list[i]+rango].get_long()))

            direction = ""

            if degres< 130.0 or degres > 220.0:
                if degres < 180:
                    direction = "Left"
                else:
                    direction = "Right"
                print("{}:   {} - > {},{} ->{}".format(direction, degres,position[self.__arr[i]].get_lat(),position[self.__arr[i]].get_long(), get_name_google(position[self.__arr[i]].get_lat(), position[self.__arr[i]].get_long())))

    def result(self):
        self.__storage.sort(key=lambda x: x[0])#sort order
        return self.__storage

#print results
# for i in intersection:
#     print("{}\n ".format(i))
#
# print("--- %s seconds ---" % (time.time() - start_time))