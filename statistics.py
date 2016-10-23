import json
import pandas as pd
from geopy.distance import vincenty
from geopy.geocoders import Nominatim

class Stats(object):
    def __init__(self):
        self.geolocator = Nominatim()

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
        address = self.geolocator.geocode(query_addr + ", Warszawa")
        query_coord = (address.latitude, address.longitude)

        places = []
        for place in query['results']:
            location = place['location']
            coordinates = (location['lat'], location['long'])
            details = (place['name'], place['address'], self.map_category(place['type']), place['rating'], vincenty(query_coord, coordinates).meters)
            places.append(details)

        df = pd.DataFrame(places, columns=['name', 'address', 'category', 'rating', 'distance'])
        categories = df.groupby('category')

        stats = {}
        radius = 3.0
        for g in categories.groups:
            if g:
                ratings = categories.get_group(g).sort_values(by='distance')[:5]['rating']
                print(type(ratings.fillna(3).mean().item()))
                stats[g] = {
                    'average_from_five': round(ratings.fillna(3).mean().item(),2),
                    'closest': round(categories.get_group(g).sort_values(by='distance')[:1]['distance'],2),
                    'places_in_radius': float((categories.get_group(g)['distance']<radius*1000).sum()),
                    'radius': radius
                }
        return stats
