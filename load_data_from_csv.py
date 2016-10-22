import pandas as pd

from database import session, Place


def load_data(csv):
    current_session = session()

    data = pd.DataFrame.from_csv(csv)

    for index, row in data.iterrows():
        place = Place(id=row['id'], name=row['name'], address=row['address'], lat=row['lat'], long=row['lon'],
                      rating=row['rating'], type=row['type'])
        current_session.add(place)

    current_session.commit()

if __name__ == '__main__':
    load_data()
