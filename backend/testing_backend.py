from app import *
from flask import Flask, request, jsonify
from app import App
import json
from utils import *
import unittest
api = Flask(__name__)
app = App(api)

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import text

# NOTE: Although some developers discourage using the real database in testing 
# (and prefer using a new, test database), since our web-app is highly stateful, 
# our tests need to interact with a real database in order to do a good job 
# testing our app's logic. Also, sanitation of user input is handled through the API
# so we are not testing here for bad input.


myapp = App(Flask(__name__))

failed_tests = {}

def test_get_restaurants(app, name, cuisine_filter, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected):

    restaurants = app.get_restaurants(cuisine_filter, price_filter, duck_bux_filter, meal_points_filter, hours_filter)

    print()
    # print("*********")
    result = len(restaurants[1])
    passed = result == expected
    if not passed:
        failed_tests[name] = {'name': name, 'result': result}

    # if passed:
    #     print(f"get_restaurants with - {name} - passed by producing {expected} restaurants")
    # else:
    #     print(f"get_restaurants with - {name} - failed to produce {expected} results. Produced {result} restaurants instead")
    # print("*********")
    return result

def test_select_all(app, name, restaurant_ids, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected):

    restaurants = app.select_all(restaurant_ids, price_filter, duck_bux_filter, meal_points_filter, hours_filter)

    result = len(restaurants)
    passed = result == expected
    if not passed:
        failed_tests[name] = {'name': name, 'result': result}
    
    return result

def test_get_cuisines(app, name, expected):

    cuisines = app.get_cuisines()

    result = len(cuisines[1])
    passed = result == expected
    if not passed:
        failed_tests[name] = {'name': name, 'result': result}
    
    return result

def test_get_relationship(app, name, cuisine_filter, expected):

    relationship = app.get_relationship(cuisine_filter)

    result = len(relationship)
    passed = result == expected
    if not passed:
        failed_tests[name] = {'name': name, 'result': result}
    
    return result

def test_get_prices(app, name, expected):

    prices = app.get_prices()

    result = len(prices)
    passed = result == expected
    if not passed:
        failed_tests[name] = {'name': name, 'result': result}
    
    return result


def main():

    test_name = "Default filters"
    cuisine_filter = None
    price_filter = None
    duck_bux_filter = None
    meal_points_filter = None
    hours_filter = False
    # There are 68 restaurant entries so get_restaurants without a filter should return all 68
    expected = 68
    total = test_get_restaurants(myapp, test_name, cuisine_filter, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected)


    # ************** Testing get_restaurants with all cuisine filter options ****************
    cuisines = myapp.get_cuisines()
    cuisines_count = len(cuisines[1])

    # Note: cuisine type #4, breakfast, was not used so it should return all 68 restaurants (the expected result when no restaurants match the given filter)
    expected = [0, 2, 8, 11, 68, 5, 30, 21, 5, 13, 4, 1, 6, 8, 17, 25, 13, 19, 7, 8]
    assert cuisines_count == len(expected)


    for i in range(1, cuisines_count):
        test_name = "cuisine filter " + str(i)
        cuisine_filter = [i]
        test_get_restaurants(myapp, test_name, cuisine_filter, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected[i])    


# ************** Testing get_restaurants with all price filter options ****************
    cuisine_filter = None
    duck_bux_filter = None
    meal_points_filter = None
    hours_filter = False
    price_count = 7
    cuisine_total = 0

    cuisine_expected = [0, 13, 24, 23, 6, 2, 68]
    # expected = [0, 7, 14, 16, 4, 24, 13]
    cuisine_len = len(cuisine_expected)
    assert price_count == cuisine_len
    for i in range(cuisine_len-1):
        cuisine_total += cuisine_expected[i]
    assert cuisine_total == total


    for i in range(1, price_count):
        test_name = "price filter " + str(i)
        price_filter = [i]
        test_get_restaurants(myapp, test_name, cuisine_filter, price_filter, duck_bux_filter, meal_points_filter, hours_filter, cuisine_expected[i]) 


# ************** Testing get_restaurants with duck_bux filter options ****************
    cuisine_filter = None
    price_filter = None
    meal_points_filter = None
    hours_filter = False

    duck_bux_filter = True
    expected = 33

    test_name = "duck_bux filter "
    test_get_restaurants(myapp, test_name, cuisine_filter, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected) 


# ************** Testing get_restaurants with meal_points filter options ****************
    cuisine_filter = None
    price_filter = None
    duck_bux_filter = None
    hours_filter = False

    meal_points_filter = True
    expected = 16

    test_name = "meal_points filter "
    test_get_restaurants(myapp, test_name, cuisine_filter, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected) 


# ************** Testing get_restaurants with hours filter options ****************
    cuisine_filter = None
    price_filter = None
    duck_bux_filter = None
    meal_points_filter = None

    hours_filter = False
    # This expected result might change based on what time of day you decide to run the tests, 
    # since this is literally telling you which restaurants are open
    expected = 68

    test_name = "hours filter "
    test_get_restaurants(myapp, test_name, cuisine_filter, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected) 



# ************** Testing select_all() with default filter options ****************
    cuisine_filter = None
    price_filter = None
    duck_bux_filter = None
    meal_points_filter = None
    hours_filter = False
    restaurant_ids = []
    for i in range(1,69):
        restaurant_ids.append(i)

    # should return all 68 restaurants
    expected = 68

    test_name = "select_all default filters"
    test_select_all(myapp, test_name, restaurant_ids, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected)


# ************** Testing select_all() with no restaurant ids options ****************
    cuisine_filter = None
    price_filter = None
    duck_bux_filter = None
    meal_points_filter = None
    hours_filter = False
    restaurant_ids = []

    # if no restaurants match cuisine filters, it should return all 68 restaurants
    expected = 68

    test_name = "select_all no restaurant ids"
    test_select_all(myapp, test_name, restaurant_ids, price_filter, duck_bux_filter, meal_points_filter, hours_filter, expected)


# ************** Testing get_cuisines() with default filter options ****************
    
    # Should return all 20 different cuisine types
    expected = 20

    test_name = "get_cuisines"
    test_get_cuisines(myapp, test_name, expected)


# ************** Testing get_relationship() for each cuisine type ****************
    
    cuisine_ids = []
    for i in range(1,21):
        cuisine_ids.append(i)

    # Testing against known number of restaurants for each cuisine
    expected = [0, 2, 8, 11, 0, 5, 30, 21, 5, 13, 4, 1, 6, 8, 17, 25, 13, 19, 7, 8, 1]

    for i in range(1, len(expected)):
        test_name = "get_relationship " + str(i)
        cuisine_filter = [i]
        test_get_relationship(myapp, test_name, cuisine_filter, expected[i])

 

    if len(failed_tests) > 0:
        print('\n\nFAILED TESTS')
        print('============\n')
        for failed in failed_tests.values():
            print('{0}\nresult: {1}\n\n'.format(failed['name'], failed['result']))
    else:
        print('\n\nALL TESTS PASSED\n\n')

if __name__ == '__main__':
    main()