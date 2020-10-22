from google import get_name_google
from getgpx import get_points
from distance import distance
from multiprocessing.pool import ThreadPool#multi process
import gpxpy
import time
import threading
from searcher import *
from getgpx import *

from multiprocessing import Process#to run concurrently.

start_time = time.time()#record time
#get the points from the gpx file
file = open('09_27_20.gpx', 'r')#for testing, it won't be here for final version
parseado = gpxpy.parse(file)
list = get_points(parseado) #array of objects that hold information like lat, long, elev, time.
size = len(list)
start = 0
end = len(list)-2
points = Route(list, size)

points.add_point(0)
points.change(start, end)
points.add_point(end+1)

resultado = points.result()



print(resultado)

print("--- %s seconds ---" % (time.time() - start_time))