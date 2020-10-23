from getgpx import get_points
import gpxpy
from math import cos, sin, asin, radians, sqrt


def distance(ini_lat, ini_lon, fin_lat, fin_lon):
	dif_lat = radians(ini_lat) - radians(fin_lat)
	dif_lon = radians(ini_lon) - radians(fin_lon)
	earth_radio = 6371 #radius in km
	distance = (sin(dif_lat/2))**2 + cos(radians(ini_lat)) * cos(radians(fin_lat)) * (sin(dif_lon/2))**2
	distancia = earth_radio * asin(sqrt(distance)) * 2 * 1000 # multiply by 1000 to convert to 	distance in meters
	return distancia


def route_distance(start, end):
	segment = 0
	for i in range(start,end):
		segment+=distance(list[i].get_lat(), list[i].get_long(), list[i+1].get_lat(), list[i+1].get_long())
	return segment
