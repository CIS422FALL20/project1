from distance import distance
from directions import get_name_tamu
from google import get_name_google
from getgpx import get_points
from nose.tools import *
import gpxpy
from angle import get_angle

# # #test distance examples
# example1 = [ 44.588692,-123.268276,44.588787,-123.262550]#  457.48 meters  west east
# result_distance1 = 457.48
# example2 = [ 44.578722,-123.283039, 44.575484,-123.277778]#549.37 meters diagonal
# result_distance2 = 549.37
# example3 = [ 44.577155, -123.292407, 44.577111,-123.283148]#732.37 metes west east
# result_distance3 = 732.37
# example4 = [ 44.077009, -123.047404, 44.063810,-123.048803]#1474.25 meters north and south
# result_distance4 = 1474.25
#
# delta = 10.0 #tolerence in distance 10 meteres plus or less
# # #test distancia
# print ("{:.2f} meters".format(distance(example1[0], example1[1], example1[2], example1[3])))
# assert_almost_equal(distance(example1[0], example1[1], example1[2], example1[3]),result_distance1, delta=delta)
# print ("{:.2f} meters".format(distance(example2[0], example2[1], example2[2], example2[3])))
# assert_almost_equal(distance(example2[0], example2[1], example2[2], example2[3]),result_distance2, delta=delta)
# print ("{:.2f} meters".format(distance(example3[0], example3[1], example3[2], example3[3])))
# assert_almost_equal(distance(example3[0], example3[1], example3[2], example3[3]),result_distance3, delta=delta)
# print ("{:.2f} meters".format(distance(example4[0], example4[1], example4[2], example4[3])))
# assert_almost_equal(distance(example4[0], example4[1], example4[2], example4[3]),result_distance4, delta=delta)

#test create object Points, create array and storage in memory all the points.
file = open('09_27_20.gpx', 'r')
parseado = gpxpy.parse(file)
position = get_points(parseado)#array of objects that hold information like lat, long, elev, time.
print(len(position))

for i in range(1,len(list)-5):
    print("{} {} : {} - {} {}".format(list[i], i, get_angle( (position[list[i-5]].get_lat(),position[list[i-5]].get_long()) , (position[list[i]].get_lat(), position[list[i+5]].get_long()) , (position[list[i+5]].get_lat(), position[list[i+15]].get_long()) ), position[list[i]].get_lat() ,position[list[i]].get_long()))

#test search an specific point by index
# number = 8770
# lat = position[number].get_lat()
# long = position[number].get_long()
# print(get_name_google(lat, long))

# #set range from where we want to get points.
# start = 0
# end = len(position)-1
# #prints points from the gpx or points and names. uncomment to change the result.
# for i in range(start,end):
#     # print("location{0}= [{1},{2}]".format(i-70, position[i].get_lat(), position[i].get_long()))
#     # line.append([position[i].get_lat(), position[i].get_long()])
#     print("{0}:  {1},{2}".format(i, position[i].get_lat(), position[i].get_long()))
#     # print('{0} -> Lat/Long: {1},{2}--> Street: {3}'.format(i, position[i].get_lat(), position[i].get_long(), get_name_google(position[i].get_lat(), position[i].get_long())))
