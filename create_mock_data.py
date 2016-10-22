import uuid

from database import session, Place


def create_mock_data():
    current_session = session()
    place = Place(id=uuid.uuid4(), name='Jakies miejsce')
    current_session.add(place)
    current_session.commit()

if __name__ == '__main__':
    create_mock_data()
