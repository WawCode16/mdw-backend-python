import json
from itertools import chain

import pandas as pd
from geopy.distance import vincenty
from geopy.geocoders import Nominatim


geolocator = Nominatim()


def warsaw_address_to_coord(address):
    return address_to_coord(address + ", Warszawa")

def address_to_coord(address):
    address = geolocator.geocode(address)
    return address.latitude, address.longitude


class Stats(object):
    def __init__(self):

    def map_category(self, place_type):
        category = ''
        if place_type in ['apteka', 'hospital']:
            category = 'health'
        elif place_type in ['park']:
            category = 'leisure'
        elif place_type in ['kino']:
            category = 'entertainment'
        elif place_type in ['cafe', 'restaurant']:
            category = 'dining'
        elif place_type in ['uniwersytet']:
            category = 'education'
        return category

    def get_stats(self, query_addr, query):
        query_coord = warsaw_address_to_coord(query_addr)
        places = [(
            place['name'],
            place['address'],
            self.map_category(place['type']),
            place['rating'],
            vincenty(query_coord, (place['location']['lat'], place['location']['long'])).meters
        ) for place in query['results']]

        df = pd.DataFrame(places, columns=['name', 'address', 'category', 'rating', 'distance'])
        categories = df.groupby('category')

        stats = {}
        radius = 3.0
        for g in categories.groups:
            if g:
                ratings = categories.get_group(g).sort_values(by='distance')[:5]['rating']
                stats[g] = {
                    'average_from_five': round(ratings.fillna(3).mean().item(),2),
                    'closest': round(categories.get_group(g).sort_values(by='distance')[:1]['distance'].item(), 2),
                    'places_in_radius': float((categories.get_group(g)['distance']<radius*1000).sum()),
                    'radius': radius
                }
        return stats
