import calendar
import json
import datetime
import os
from flask import Flask
from models import Restaurants, Relationships, Cuisines, Hours, Submissions
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, inspect
from utils import setup_log, log
import traceback


class App:
    def __init__(self, flask_instance):
        '''initialize App by connecting to restaurants.db database'''
        try:
            #connect to the database
            flask_instance.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'

            #Per SQLAlchemy documentation
            flask_instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

            #start first day of week on Monday consistent with database setup
            calendar.setfirstweekday(calendar.MONDAY)

            #start the SQLAlchemy engine and create pool of resources
            #please see the backend.md documentation for more information regarding the resource pool
            self.database = SQLAlchemy(flask_instance)
            log("New App instance initialized")
            
        except BaseException:
            log("App Initialization Error")
            return None

    def __new__(cls, flask_instance):
        '''Perform Basic argument validation and setup checking prior to initializaiton of app'''

        # setup logging
        setup_log()

        # ensure __init__ has valid arguments before class creation
        if not isinstance(flask_instance, Flask):
            log("App Initialization Error, Invalid __init__ arguments: Not a flask instance")
            return None

        # ensure the restaurants database exists
        if not os.path.exists('./restaurants.db'):
            log("Database Missing, Attempting to Create Database")
            try:
                import db_setup
                if not os.path.exists('./restaurants.db'):
                    log("App Initialization Error, Unable to Setup Database")
                    return None
            except BaseException:
                log("App Initialization Error, Unable to Setup Database")
                return None

        # proceed with initialization
        return object.__new__(cls)

    def get_restaurants(
            self,
            cuisine_filter=None,
            price_filter=None,
            duck_bux_filter=None,
            meal_points_filter=None,
            hours_filter=False):
            
        '''This is the main entrypoint for datbase queries.
        Function argument and return value descriptions can
        be found in the backend.md documentation.
        '''
        try:
            # log
            log("Requested Recieved in get_restaurants")

            # filter on cuisine first to get restaurant list
            restaurant_ids = self.get_relationship(cuisine_filter)
            log("completed get_relationship")

            #use rest of filters on restaurant list
            restaurant_query = self.select_all(restaurant_ids, price_filter, duck_bux_filter, meal_points_filter, hours_filter)
            code = 0
            if len(restaurant_query) == 0:
                code = 1
                restaurant_ids = self.get_relationship(None)
                restaurant_query = self.select_all(restaurant_ids, None, None, None, None)
            log("completed select_all")

            # initialize restuarant list as empty
            restaurant_dictionary_list = []

            # each instance of the restuarant class now contains all required information, we just need to format that information into a dictionary
            # iterate over each Restaurant instance returned from select_all
            for restaurant in restaurant_query:

                # get key/value pairs for all class variables
                restaurant_dict = vars(restaurant).copy()

                # get the SQAlchemy instance variable
                sqlalchemy_instance = inspect(restaurant)

                # remove the SQLAlchemy instance variable from the dictionary
                for key, value in restaurant_dict.items():

                    # compare with the current value
                    if value == sqlalchemy_instance:
                        del restaurant_dict[key]

                        # to prevent runtime error, break after changing the size of the dictionary
                        # this also removes the one and only instance of the
                        # SQLAlchemy variable
                        break

                # append the formatted dictionary
                restaurant_dictionary_list.append(restaurant_dict)

            return code, restaurant_dictionary_list
        except Exception as e:
            log(traceback.format_exc())
            log("Error processing request in get_restaurants")
            return 1, []

    def select_all(
            self,
            restaurant_ids,
            price_filter,
            duck_bux_filter,
            meal_points_filter,
            hours_filter):

        '''select_all applies the given filters to a database query.
        This query is them formatted through the use of helper functions.

        Function argument and return value descriptions can
        be found in the backend.md documentation.
        '''

        # log
        log("start select_all")

        # list of all possible filters declared as empty
        boolean_filters = []
        price_list = []
        restaurants_filter = []

        # for each of the boolean filters, reformat them as SQLAlchemy filter
        # queries
        if duck_bux_filter is not None:
            boolean_filters.append(Restaurants.duck_bux == duck_bux_filter)
        if meal_points_filter is not None:
            boolean_filters.append(
                Restaurants.meal_points == meal_points_filter)

        # for each of the price filters in the price_filter list, reformat them
        # as SQLAlchemy filter queries
        if price_filter is not None:
            for price in price_filter:
                price_list.append(Restaurants.price == price)

        # for each of the cuisine filters in the restaurant_ids list, reformat
        # them as SQLAlchemy filter queries
        if restaurant_ids is not None:
            for restaurant_id in restaurant_ids:
                restaurants_filter.append(
                    Restaurants.restaurant_id == restaurant_id)

        # query the database with the selected filters
        restaurants_list = self.database.session.query(Restaurants).filter(
            and_(or_(*price_list), or_(*restaurants_filter), (*boolean_filters))).all()
        log("in select_all, # of restaurants post query to Restaurants database = {}".format(
            len(restaurants_list)))

        # for each restuarant in list, replace hours with human readable hours
        restaurants_list = self.format_hours(restaurants_list, hours_filter)
        log("completed format_hours")

        if hours_filter:
            log("in select_all, # of restaurants post removal of closed restaurant = {}".format(
                len(restaurants_list)))

        # for each restaurant in list, replace integers in cuisines with actual
        # cuisines
        restaurants_list = self.format_cuisines(restaurants_list)
        log("completed format_cuisines")

        restaurants_dict = {}
        restaurants_dict['restaurants'] = restaurants_list

        return restaurants_list

    def format_cuisines(self, restaurants_list):
        '''
        (list) -> list      Called by select_all
        Takes in a list of restaurants, replaces list
        of cuisine id's with a list of actual cuisines.
        Returns updated restaurant list.
        '''

        # log
        log("start format_cuisines")

        cuisines_list = []
        cuisines_list = self.get_cuisines()

        for restaurant in restaurants_list:
            restaurants_cuisine_list = []

            num_list = restaurant.cuisines
            for num in num_list:
                # if cuisines already in there, exit this function:
                if not isinstance(num, int):
                    return restaurants_list
                # Add the corresponding cuisine to the restaurant's cuisine
                # list
                restaurants_cuisine_list.append(cuisines_list[1].get(num))

            # Put the new cuisine list in the correct spot in the current
            # restaurant's list
            restaurant.cuisines = restaurants_cuisine_list

        return restaurants_list

    def restaurant_is_open(self, hours_data):
        '''Called by format_hours()
        Returns a boolean indicating whether the current system time
        falls within the operational hours given in hours_data

        Function argument and return value descriptions can
        be found in the backend.md documentation.
        '''

        # get the current system time
        time_now = datetime.datetime.now()

        # cycle through all open hours for all days of the week
        for hour in hours_data:

            # find the buisness hours for today
            # note, weekday() starts with Monday at 0 and Sunday at 6
            # thus conforming with the database standard
            if time_now.date().weekday() == hour.day_of_week:

                # format the open/close hours from the database
                open_hours = datetime.time(
                    hour=int(hour.restaurant_open[:2]), minute=int(hour.restaurant_open[3:]))
                close_hours = datetime.time(
                    hour=int(hour.restaurant_close[:2]), minute=int(hour.restaurant_close[3:]))

                # determine if the given restuarant is open
                if open_hours < time_now.time() and close_hours > time_now.time():

                    # if it is currently open, return true. No need to continue
                    # checking
                    return True

        # return false if no positive match is found in all the hours given
        return False

    def format_hours(self, restaurants_list, hours_filter):
        '''Queries the hours database for each restaurant in the 
        restaurants_list and formats the query results into a human
        readable string.

        Function argument and return value descriptions can
        be found in the backend.md documentation.
        '''

        # log
        log("start format_hours")

        #restaurants_list position starts at 0
        position = 0

        # for each restaurant in list, replace integers in hours with human readable hours
        while position < len(restaurants_list):

            #Query the database for hours for that restaurant
            hours_query = self.database.session.query(Hours).filter_by(restaurant_id=restaurants_list[position].restaurant_id).all()

            if hours_filter:
                if self.restaurant_is_open(hours_query) == False:
                    restaurants_list.remove(restaurants_list[position])
                    continue            

            # Outline for hours format
            restaurant_hours = {}

            # get all hours on a specific day
            for hour in hours_query:
                if calendar.day_name[hour.day_of_week] in restaurant_hours.keys(
                ):
                    restaurant_hours[calendar.day_name[hour.day_of_week]] = (restaurant_hours.get(
                        calendar.day_name[hour.day_of_week]) + ", " + self.twenty_four_to_standard(hour.restaurant_open) + " - " + self.twenty_four_to_standard(hour.restaurant_close))

                else:
                    restaurant_hours[calendar.day_name[hour.day_of_week]] = (   self.twenty_four_to_standard(hour.restaurant_open)
                        + " - " + self.twenty_four_to_standard(hour.restaurant_close)   )

            #ensure we have data for each day
            for i in range(7):
                if restaurant_hours.get(calendar.day_name[i]) == None:
                    restaurant_hours[calendar.day_name[i]] = "CLOSED"

            #turn that data into human readable string
            readable_hours = ''
            for i in range(7):
                readable_hours = readable_hours + calendar.day_name[i] + ": " + restaurant_hours.get(calendar.day_name[i])
                if i != 6:
                    readable_hours = readable_hours + '\n'

            #assign the value to the restaurants_list
            restaurants_list[position].hours = readable_hours

            position = position + 1
        
        return restaurants_list

    def twenty_four_to_standard(self, military_time_string):
        '''Given a military time formatted string,
        returns a 12hour formatted time string.

        Function argument and return value descriptions can
        be found in the backend.md documentation.
        '''
        # create datetime object
        formated_time_string = datetime.time(
            hour=int(military_time_string[:2]), minute=int(military_time_string[3:]))

        # return 12hour string
        formated_time_string = formated_time_string.strftime("%l:%M%p")

        return formated_time_string

    def get_cuisines(self):
        '''Queries the Cuisines database and returns a dictionary
        of all types therein.

        Function argument and return value descriptions can
        be found in the backend.md documentation.
        '''

        # log
        log("start get_cuisines")
        try:
            cuisines_dict = {}
            for cuisine in self.database.session.query(Cuisines).all():
                cuisines_dict[cuisine.cuisine_id] = cuisine.name

            return 0, cuisines_dict
        except BaseException:
            # log
            log("Error in get_cuisines")
            return 1, {}

    def get_prices(self):

        '''Queries the Restaurants.price database and returns 
        a dictionary of all types therein.

        Function argument and return value descriptions can
        be found in the backend.md documentation.
        '''

        # log
        log("start get_prices")
        try:
            return [
                price for (
                    price,
                ) in self.database.session.query(
                    Restaurants.price).distinct()]
        except BaseException:
            # log
            log("Error in get_prices")
            return []

    def get_relationship(self, cuisine_filter):
        '''Given a list of cuisine_types, returns a list of 
        restaurant_ids that serve that cuisine type.

        Function argument and return value descriptions can
        be found in the backend.md documentation.
        '''

        # log
        log("start get_relationship")

        # return None if the filter was empty
        if cuisine_filter is None:
            return None

        restaurant_ids = []
        try:
            for id in cuisine_filter:
                # make a list of each unique restaurant id related to the
                # cuisine id
                for relationship in self.database.session.query(
                        Relationships).filter(Relationships.cuisine_id == id).all():
                    if relationship.restaurant_id not in restaurant_ids:
                        restaurant_ids.append(relationship.restaurant_id)
            return restaurant_ids

        except BaseException:
            log("Error in get_relationship")
            return 0

    def handle_submission(self, email='', comment=''):
        # log
        log("start handle_submission")
        self.database.session.add(Submissions(email=email, comment=comment))
        self.database.session.commit()

    def get_submissions(self):
        # log
        log("start get_submission")
        return [row.__dict__ for row in self.database.session.query(
            Submissions).all()]
