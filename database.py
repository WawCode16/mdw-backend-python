from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://postgres@db:5432/postgres')

Base = declarative_base()


class Place(Base):
    __tablename__ = 'place'
    id = Column(String, primary_key=True)
    name = Column(String)
    address = Column(String)
    lat = Column(Float, index=True)
    long = Column(Float, index=True)
    type = Column(String)
    rating = Column(Float)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'location': {
                'lat': self.lat,
                'long': self.long
            },
            'type': self.type,
            'rating': self.rating
        }


class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class PlaceType(Base):
    __tablename__ = 'placetype'
    place_id = Column(String, ForeignKey('place.id'), primary_key=True)
    type_id = Column(Integer, ForeignKey('type.id'), primary_key=True)
    place = relationship(
        Place,
        backref=backref('placetypes', uselist=True, cascade='delete,all'))
    type = relationship(
        Type,
        backref=backref('placetypes', uselist=True, cascade='delete,all'))


def create_database():
    print("Creating database...")
    Base.metadata.create_all(engine)
    print("Database created!")

session = sessionmaker()
session.configure(bind=engine)
