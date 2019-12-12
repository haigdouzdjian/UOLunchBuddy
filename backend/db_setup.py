import csv
from utils import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import os

setup_log()
start = time.time()

if os.path.exists('./restaurants.db'):
    os.remove('restaurants.db')

api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
database = SQLAlchemy(api)


class Restaurants(database.Model):
    restaurant_id = database.Column(
        database.Integer,
        primary_key=True,
        autoincrement=True)
    name = database.Column(database.String(255), nullable=False)
    cuisines = database.Column(database.JSON)
    coordinates = database.Column(database.String(255))
    location = database.Column(database.String(255))
    duck_bux = database.Column(database.Boolean)
    meal_points = database.Column(database.Boolean)
    price = database.Column(database.Integer)


class Cuisines(database.Model):
    cuisine_id = database.Column(
        database.Integer,
        primary_key=True,
        autoincrement=True)
    name = database.Column(database.String(255))


class Hours(database.Model):
    restaurant_id = database.Column(database.Integer, primary_key=True)
    day_of_week = database.Column(database.Integer, primary_key=True)
    restaurant_open = database.Column(database.String(255), primary_key=True)
    restaurant_close = database.Column(database.String(255), primary_key=True)


class Relationships(database.Model):
    relationship_id = database.Column(database.Integer, primary_key=True)
    restaurant_id = database.Column(database.Integer)
    cuisine_id = database.Column(database.Integer)


class Submissions(database.Model):
    email = database.Column(database.String(255), primary_key=True)
    comment = database.Column(database.String(1023), primary_key=True)


database.create_all()

with open('data/cuisines.txt', 'r') as f:
    for line in f:
        line = line.replace('\n', '')
        cuisine = Cuisines(name=line)
        database.session.add(cuisine)

cuisine_map = {c.name: c.cuisine_id for c in Cuisines.query.all()}

with open('data/restaurants.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        name = line[0]
        cuisine_ids = [cuisine_map[i] for i in line[1].split(',')]
        # Save ID into a dictionary
        coordinates = line[2].replace(' ', '')
        location = line[3]
        duck_bux = True if line[4] == 'Yes' else False
        meal_points = True if line[5] == 'Yes' else False
        price = line[6]

        restaurant = Restaurants(
            name=name,
            cuisines=cuisine_ids,
            coordinates=coordinates,
            location=location,
            duck_bux=duck_bux,
            meal_points=meal_points,
            price=price
        )

        database.session.add(restaurant)

# makes a database of restaurants
restaurant_ids = {r.name: r.restaurant_id for r in Restaurants.query.all()}

days = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday']
with open('data/hours.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        restaurant_id = restaurant_ids[line[0]]
        start_day = days.index(line[1].split('-')[0])
        try:
            end_day = days.index(line[1].split('-')[1])
        except BaseException:
            end_day = start_day

        for day in range(start_day, end_day + 1):
            hour = Hours(
                restaurant_id=restaurant_id,
                day_of_week=day,
                restaurant_open=line[2],
                restaurant_close=line[3]
            )
            database.session.add(hour)

# makes a dic of cuisines
cuisine_ids = {r.name: r.cuisine_id for r in Cuisines.query.all()}
with open('data/restaurants.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        restaurant_id = restaurant_ids[line[0]]
        cuisines_list = (line[1].split(','))
        for cuisine in cuisines_list:
            clean_cuisine = cuisine.strip()
            cuisine_id = cuisine_ids[clean_cuisine]
            filtered_cuisine = Relationships(
                restaurant_id=restaurant_id,
                cuisine_id=cuisine_id
            )
            database.session.add(filtered_cuisine)

database.session.commit()
database.session.close()

log('Created DB in {:.3f} sec'.format(time.time() - start))
