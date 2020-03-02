import math
from collections import namedtuple

EARTH_RADIUS = 6378137 # metres
EARTH_CIRCUMFERENCE  = 40075000 # metres
MAX_DISTANCE = EARTH_CIRCUMFERENCE / 2 # metres

def radian(coordinate):
    return (math.pi * coordinate) / 180

def distance(coordinates_1, coordinates_2):
     '''
     This function returns the distance between two pairs of latitude and longitude coordinates using the Haversine Formula (https://en.wikipedia.org/wiki/Haversine_formula).
     '''

     latitude_dist = radian(coordinates_2[0] - coordinates_1[0])
     longitude_dist = radian(coordinates_2[1] - coordinates_1[1])

     a = (math.sin(latitude_dist / 2) * math.sin(latitude_dist / 2)) + math.cos(radian(coordinates_1[0])) * math.cos(radian(coordinates_2[0])) * \
          math.sin(longitude_dist / 2) * math.sin(longitude_dist / 2)

     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

     distance = EARTH_RADIUS * c

     return round(distance, 5)

def stress(cache_info):
     '''
     This function returns a float between -1 and 1 representing the stress score based on the NamedTuple passed as cache info.
     A stress score near -1 means the cache represented by the cache info is not stressed at all (and might be redundant), near 0 means the cache is experiencing normal stress, and near 1 means the cache is experiencing high stress.
     The stress score depends on the number of hits, misses, evictions and expiries.
     A cache info with more hits and evictions, and fewer misses and expiries is more highly stressed than its counterpart with fewer hits and evictions, and more misses and expiries.
     The stress score is used to calculate which proxy would benefit most from having an additional proxy deployed nearby to takeover some of its assigned clients.
     '''
     # TODO should take into account (1 - curr_size / max_size) as a penalty on the score
     return ((cache_info.hits + cache_info.evictions) - (cache_info.expiries + cache_info.misses)) / (cache_info.hits + cache_info.evictions + cache_info.expiries + cache_info.misses)