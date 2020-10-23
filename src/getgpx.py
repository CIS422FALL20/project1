#data structure that hols
import gpxpy

#I prefer to use a class instead of a dict since allows to extends easily in future if required. Names are more clear to indicate its parts.

class Puntos:#class that holds info of one point. The idea is create an array of this object.
    def __init__(self,lat, long, elev, time):
        self.__lat = lat
        self.__long = long
        self.__elev = elev
        self.__time = time

    def get_lat(self):
        return self.__lat

    def get_long(self):
        return self.__long

    def get_elev(self):
        return self.__elev

    def get_time(self):
        return self.__time

#it creates an array of Puntos and return an array with all the coordinates in the gpx file.
def get_points(parseado):
    contador = 0
    position = []

    for track in parseado.tracks:
        for segment in track.segments:
            for point in segment.points:
                position.append(Puntos(point.latitude, point.longitude, point.elevation, point.time))
                contador+=1

    return position
