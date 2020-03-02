import math

EARTH_RADIUS = 6378137 # metres
EARTH_CIRCUMFERENCE  = 40075000 # metres
MAX_DISTANCE = EARTH_CIRCUMFERENCE / 2 # metres

def radian(coordinate):
    return (math.pi * coordinate) / 180

def distance(coordinates_1, coordinates_2):
     """
     This function returns the distance between two pairs of latitude and longitude coordinates using the Haversine Formula (https://en.wikipedia.org/wiki/Haversine_formula)
     """

     latitude_dist = radian(coordinates_2[0] - coordinates_1[0])
     longitude_dist = radian(coordinates_2[1] - coordinates_1[1])

     a = (math.sin(latitude_dist / 2) * math.sin(latitude_dist / 2)) + math.cos(radian(coordinates_1[0])) * math.cos(radian(coordinates_2[0])) * \
          math.sin(longitude_dist / 2) * math.sin(longitude_dist / 2)

     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

     distance = EARTH_RADIUS * c

     return round(distance, 5)