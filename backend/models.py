from sqlalchemy import Column, Integer, String, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cuisines(Base):
    __tablename__ = 'Cuisines'

    cuisine_id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)

    def __repr__(self):
        return '<Cuisine %r>' % self.name


class Restaurants(Base):
    __tablename__ = 'Restaurants'

    restaurant_id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    cuisines = Column(JSON)
    coordinates = Column(String(255))
    location = Column(String(250))
    duck_bux = Column(Boolean)
    meal_points = Column(Boolean)
    price = Column(Integer)

    def __repr__(self):
        return '< RESTAURANT: %r,%r,%r,%r,%r,%r>' % (
            self.name, self.cuisines, self.location, self.duck_bux, self.meal_points, self.price)


class Hours(Base):
    __tablename__ = 'Hours'

    restaurant_id = Column(Integer, primary_key=True)
    day_of_week = Column(Integer, primary_key=True)
    restaurant_open = Column(String(250), primary_key=True)
    restaurant_close = Column(String(250), primary_key=True)

    def __repr__(self):
        return '<%r %r %r %r>' % (self.restaurant_id,
                                  self.day_of_week,
                                  self.restaurant_open,
                                  self.restaurant_close)


class Relationships(Base):
    __tablename__ = 'Relationships'

    relationship_id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, primary_key=True)
    cuisine_id = Column(Integer, primary_key=True)
    # name = Column(String(250), unique=True, nullable=False)

    def __repr__(self):
        return '<Relationship: Restaurant ID %r: Cuisine ID %r>' % (
            self.restaurant_id, self.cuisine_id)


class Submissions(Base):
    __tablename__ = 'Submissions'

    email = Column(String(255), primary_key=True)
    comment = Column(String(1023), primary_key=True)

    def __repr__(self):
        return '<Submission: Email: %r Comment: \"%r\"' % (
            self.email, self.comment)
