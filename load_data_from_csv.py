import math
import pandas as pd

from database import session, Place


def get_type(key, data, type=None):
    try:
        value = data[key]
        value = type(value) if type else value
        return None if not isinstance(value, str) and math.isnan(value) else value
    except:
        return None


def load_data(csv):
    current_session = session()

    data = pd.DataFrame.from_csv(csv)

    for index, row in data.iterrows():
        place = Place(
            id=get_type('id', row), 
            name=get_type('name', row), 
            address=get_type('address', row), 
            lat=get_type('lat', row, float),
            long=get_type('lon', row, float),
            rating=get_type('rating', row, float),
            type=get_type('type', row)
        )
        current_session.merge(place)

    current_session.commit()
    current_session.close()

if __name__ == '__main__':
    load_data('data/apteka.csv')
