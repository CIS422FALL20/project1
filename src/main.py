import gpxpy
import time

from searcher import *
from getgpx import *

def main(f):
    start_time = time.time()  # record time
    # get the points from the gpx file
    file_ = open(f, 'r')  # for testing, it won't be here for final version
    parsed_file = gpxpy.parse(file_)
    getting_points = get_points(parsed_file)  # array of objects that hold information like lat, long, elev, time.
    points = Route(getting_points)

    end_result = points.result()
    #ret = []
    #for elem in end_result:
        #print(f"{elem[1]} {elem[3]}")
    #    if len(elem) > 0:
    #        ret.append(f"pos: {elem[0]}, address:,{elem[3]}, turning: {elem[1]}, point: ({elem[4]}, {elem[5]})")
    return end_result #ret

#print("--- %s seconds ---" % (time.time() - start_time))
