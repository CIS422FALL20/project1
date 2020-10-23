#FINDS THE TURNING POINTS, IT RETURNS THE NAMES AND THE NUMBER OF THE INDEX WHERE THE TURNS ARE.
#it gets the info  from the points from the gpx files and perform a recursion search
#to get the points where the streets changes. used the module "google" from where it connects to google
#maps and get the name of the address where some point (lat,long) is located.
#returns and 2d Array witht [gpx index number, name of streets, latitude, longitud]
#latest version (10/20/20)
from google import get_name_google
from getgpx import get_points
from distance import distance
from multiprocessing.pool import ThreadPool#multi process
import gpxpy
import time
import threading

from multiprocessing import Process#to run concurrently.

start_time = time.time()#record time
#get the points from the gpx file
file = open('09_27_20.gpx', 'r')#for testing, it won't be here for final version
parseado = gpxpy.parse(file)
list = get_points(parseado) #array of objects that hold information like lat, long, elev, time.

#first point and last one that are in the range is verify
start = 0#first point
end = len(list)-1#last point
print("Start: {} End:{}".format(start,end))#debug

pool = [""]*len(list)#cache to reduce the number of requests, collisions will prevent requesting more data.

#I eliminate the class and I am gonna use a 2d array instead.
intersection = []
#helper
def points(parts):#extract points, get the name address and add the info into the pool array(cache)

    thpool = ThreadPool(processes=1)
    interpolate = [""]*3

    for i in parts:
        if pool[i[1]] == "":#if the data is in the cache array, it will not request the data but use the one from the pool array
            async_result = thpool.apply_async(get_name_google,(list[i[1]].get_lat(), list[i[1]].get_long()))
            interpolate[i[0]] = async_result.get()#holds more than one request.
            pool[i[1]] = interpolate[i[0]]
        else:
            print("collision")



#adding starting point of the whole road
intersection.append([start, get_name_google(list[start].get_lat(), list[start].get_long()), list[start].get_lat(), list[start].get_long()])
def change(start, end, storage):#list contains all the points, start first point, end last one and storage saves the results.
    middle = int((start+end)/2)

    parts1 = [[0,start],[1,middle],[2,end]]
    points(parts1)

    # base case: when  the start, the middle and the end is the same.
    if pool[start] == pool[middle] and pool[middle] == pool[end]:
        return

    # when start and middle are equal and middle and end not equal(or viceverse), possible indication of a point of change.
    if (pool[start] == pool[middle] and  pool[middle] != pool[end]) or (pool[start] != pool[middle] and  pool[middle] == pool[end]):

        parts2 = [[0,middle+1], [1,middle-1]]
        points(parts2)

        #checks if the next point from the middle is different, if it is, change detected and added.
        if  pool[middle-1] != pool[middle]:
            storage.append([middle-1, pool[middle-1], list[middle-1].get_lat(), list[middle-1].get_long()])
        elif pool[middle] != pool[middle+1]:
            storage.append([middle, pool[middle], list[middle].get_lat(), list[middle].get_long()])
        else:
            change(start, middle, storage)
            change(middle+1, end, storage)

    else:
        parts3 = [[0,middle+1], [1,middle-1]]
        points(parts3)
        #checks when start, middle and end are different but the middle falls exactly in a changing point. it will perform the checking and add the point if it falls in the changing point.
        if pool[middle-1] != pool[middle]:
            storage.append([middle-1, pool[middle-1], list[middle-1].get_lat(), list[middle-1].get_long()])
        elif pool[middle] != pool[middle+1]:
            storage.append([middle, pool[middle], list[middle].get_lat(), list[middle].get_long()])
        #will continue dividing and searching.
        change(start, middle, storage)
        change(middle+1, end, storage)

#calling fuction, returns one list of array, "intersectation" is an array that contains the results.
change(start, end, intersection)
#adding ending point
intersection.append([end, get_name_google(list[end].get_lat(), list[end].get_long()), list[end].get_lat(), list[end].get_long()])
intersection.sort(key=lambda x: x[0])#sort order

#print results
for i in intersection:
    print("{}\n ".format(i))

print("--- %s seconds ---" % (time.time() - start_time))
