# **`UO Lunch Buddy Backend`**
### **Purpose of this Document:**

The purpose of this document is to describe the ways in which the various modules of UO Lunch Buddy Backend interact with one another and to provide context to the various function calls that are invoked during those interactions.

### **Table of Contents**

+ [app](#app)
    + [\_\_init__](#\_\_init__)
    + [get_restaurants](#get_restaurants)
    + [get_cuisines](#get_cuisines)
    + [get_prices](#get_prices)
+ [Classes](#classes)
    + [cuisines_class](#cuisines_class)
    + [restaurants_class](#restaurants_class)
    + [hours_class](#hours_class)
    + [relationships_class](#relationships_class)
    + [submissions_class](#submissions_class)
+ [db_setup](#db_setup)
+ [Naming Conventions](#Naming\ Conventions)

# **`app`**
This section provides a general descripion of the App class.

## **Description**
The App class is initialized by the UO Lunch Buddy `api` and used to query, filter and format results from the restaurants database.


To accomplish this task, the App class takes advantage an SQLAlchemy database by making use of the extension, [Flask_SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/). For a more detailed discussion on why the Flask_SQLAlchemy extension is used, please see the Software Architecture document.

# **Methods**

## **\_\_init__**
### **Description:**

The initialization of the App class requires that a Flask instance be passed in as an argument.

### **Arguments & Example:**

In this example, `Flask(__name__)` creates a flask instance, which is then passed as an initialization argument in the subsequent line `App(flask_instance)`.

```python
>>> flask_instance = Flask(__name__)

>>> app_instance = App(flask_instance)
```
### **Return Values:**

On successful initalization of all components of the app class, a new App object is returned.

If, for any reason, the initialization fails, `None` is returned.

## **get_restaurants()**

### **Description:**

The get_restaurants() method serves as the primary access point for database queries.

### **Arguments**

get_restaurants() 4 arguments are listed below:
* cuisine_filter
* price_filter
* duck_bux_filter
* meal_points_filter

 All of get_restaurants() arguments are optional. Data validation is handled within the api. Subsequently, all arguments provided are assumed to conform to the standards as described in [Naming Conventions](#Naming\ Conventions).

 Any argument that is not None represents a datapoint to which all restaurant database query results are filtered against.

 ### **Example:**

The example below illustrates how you can make use of get_restaurant's optional arguments to filter restaurant results

```python
>>> code, restaurants = app_instance.get_restaurants()
>> print(len(restaurants))

68

>>> desired_cuisines = [1,2,3]
>>> code, restaurants = app_instance.get_restaurants(cuisine_filter = desired_cuisines)
>> print(len(restaurants))

21
```

### **Return Value**

The get_restaurants() method always returns a tuple with 2 values in the format `(response_code, restaurants_list)`. 

`response_code` is an integer value whos meaning is described in the api .md documentation. 

`restaurants_list` is a list of dictionaries whos key-values pairs correspond to query results

## **get_cuisines()**

### **Description:**

This method is called by the frontend to obtain a dictionary of all cuisine types in the restaurant database

The keys of the dictionary represent valid arguments for the cuisine_filter. The values of the dictionary represent their human readable names.

### **Example:**

The example below illustrates not only how to use the get_cuisines method, but also how its keys can be used as arguments for the cuisines filter.

```python
>>> keys = app_instance.get_cuisines().keys()
>>> code, restaurants = app_instance.get_restaurants(cuisine_filter=keys)
>>> print(len(restaurants))

68
```

### **Return Value**

On successful execution, the get_cuisines() method returns a cuisines_dict. The cuisines_dict is a app specific variable whos value is described in [Naming Conventions](#Naming\ Conventions)

If the method fails for any reason, a log entry is made and an empty dictionary is returned

## **get_prices()**

### **Description:**

This method is called by the frontend to obtain a list of all restaurant price ratings in the restaurant database

The values of the list represent valid arguments for the price_filter.

### **Example:**

The example below illustrates not only how to use the get_prices method, but also how its values can be used as arguments for the price filter.

```python
>>> prices = app_instance.get_prices()
>>> code, restaurants = app_instance.get_restaurants(price_filter=prices)
>>> print(len(restaurants))

68
```

### **Return Value**

On successful execution, the get_prices() method returns a prices_list. The prices_list is a app specific variable whos value is described in [Naming Conventions](#Naming\ Conventions)

If the method fails for any reason, a log entry is made and an empty list is returned


# **`Classes`**

This section outlines the SQL_Alchemy classes used by
*UO Lunch Buddy*. It documents each class name, attributes, and any methods associated with them.

### **Cuisines_class**
The cuisines class is the associated python representation of the 'Cuisines' table in the restaurants database. Each of the twenty unique cuisines have their own entry/instance. Class cuisine has two data members:

Name | Type | Description
-----|------|------------
cuisine_id | integer | Auto-incremented primary key
name | string | Unique name of the cuisine type

The cuisines class has one method, __repr__ that prints out "Cuisine" and then the value stores in self.name - which is the name of the cuisine. Example output: <Cuisine Asian>

### **Restaurants_class**
The restaurants class is the associated python representation of the 'Restaurants' table in the restaurants database. Each of the 68 restaurants have their own entry/instance. Class restaurants has eight data members:

Name | Type | Description
-----|------|------------
restaurant_id | integer | Auto-incremented primary key
name | string | Unique name of the restaurant
cuisines | JSON | A list of integers corresponding with cuisine types
coordinates | string | Latitude,Longitude map coordinates of the restaurant
location | string | Address or campus building of the restaurant
duck_bux | boolean | True = Accepts duck bucks
meal_points | boolean | True = Accepts meal points
price | integer | 1 = up to $2, 2 = $2-$4, 3 = $4-$6, 4 = $6-$8, 5 = over $8

The restaurants class has one method, __repr__ that prints out "RESTAURANT" followed by self.name, self.cuisines, self.location, self.duck_bux, self.meal_points, self.price. Example output: <RESTAURANT: Trev's Sports Bar & Grill Pub, American, 44.046697,-123.068247, 1675 Franklin Blvd, Eugene, OR 97401, No, No, 4>

### **Hours_class**
The hours class is the associated python representation of the 'Hours' table in the restaurants database. Since each restaurant can have a different open/close schedule for each day of the week, there are sometimes multiple entries/instances for one restaurant. Class hours has four data members:

Name | Type | Description
-----|------|------------
restaurant_id | integer | Auto-incremented primary key
day_of_week | integer | 1 = Sunday 2 = Monday 3 = Tuesday 4 = Wednesday 5 = Thursday 6 = Friday 7 = Saturday
restaurant_open | string | Time restaurant opens
restaurant_close | string | Time restaurant closes

The hours class has one method, __repr__ that prints out self.restaurant_id, self.day_of_week, self.restaurant_open, self.restaurant_close. Example output: <1, 1, 10:00am, 10:00pm>

### **Relationships_class**
The relationships class is the associated python representation of the 'Relationships' table in the restaurants database. Each entry/instance represents one cuisine classification for a restaurant. Since a restaurant might serve multiple types of cuisines, there are sometimes multiple relationships for one restaurant. Class relationships has three data members:

Name | Type | Description
-----|------|------------
relationship_id | integer | Auto-incremented primary key
restaurant_id | integer | Restaurant ID from the restaurant table
cuisine_id | integer | Cuisine ID from the cuisine table

The relationships class has one method, __repr__ that prints out "Relationship: Restaurant ID: <self.restaurant_id> Cuisine ID: <self.cuisine_id>." Example output: <Relationship: Restaurant ID: 1 Cuisine ID: 3>

### **Submissions_class**
The submissions class is the associated python representation of the 'Submissions' table in the restaurants database. Each entry/instance represents one user submission. Class submissions has two data members:

Name | Type | Description
-----|------|------------
email | string | User's email address
comment | string | User's comment

The submissions class has one method, __repr__ that prints out "Submission: Email: <self.email> Comment: <self.comment>." Example output: <Submission: Email: joe@uoregon.edu Comment: Are you going to add Sabai Thai restaurant on 27 Oakway Center, Eugene, OR 97401?>


# **`db_setup`**
This section provides a general descripion of the db_setup module.

### **Description**

The db_setup module is a python script that uses the [Flask_SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) extension to setup the restaurants database.

This database is then populated with the information contained within the documents in the `/backend/data` folder. This information is processed to conform to the models schema as described in the [Classes](#Classes) section.

### **Required Documents & Example**

The db_setup script requires that the following documents be present in the /backend/data folder:

* cuisines.txt
* hours.csv
* restaurants.csv

The contents of these documents are described below:

Document | Description | Example | Remarks
---------|-------------|-----------------|--------
cuisines.txt | A list of all Cuisines in the database seperated by newlines. | Mexican <br> Italian | The order in which these cuisines are listed will determine their integer_id in the database.
hours.csv | "Restaurant name" , "Days of the Week" , "Open Time", "Close Time" | Barnhart Dining,Monday-Friday,11:00,16:30 <br><br>Barnhart Dining,Monday-Friday,17:00,20:00 | "Days of Week" field can be a specific day or a range of days, such as "Monday-Friday".<br><br> The Open and Close Times are denoted in 24 hour time.<br><br> As is seen in the example, restuarants can have multiple entries for a given day, representing breaks in hours of operation, such as when a restaurant is closed prior to serving dinner.
restaurants.csv | "Restaurant Name" , "List of Cuisines" , "coordinates" , "location" , "Accepts duck bux" , "Accepts meal points", "price rating" | Common Grounds Cafe, "Cafe, Sandwich, Market, Smoothie, Dessert,Snack", "44.045195,-123.068959", Hamilton Hall, Yes, Yes, 2| "The list of Cuisines" is a quoted, comma seperated list of Cuisines matching the entries of the cuisines.txt document. <br><br> The "Coordinates" is a quoted, comma seperated string representing the restaurants location. <br><br> "Accepts duck bux" and "Accepts meal points" are boolean `True` / `False` values <br><br> "Price rating" is a single integer corresponding to the price rating of the restuarant as described [Restaurants_class](#Restaurants_class)


# **`Naming Conventions`**
The following table describes the naming conventions of varables within the backend.

Varaible Name | Description | Remark | Example
--------------|-------------|--------|--------
flask_instance | Instance of a Flask object | Required upon initialization of the App class. | `<Flask 'api'>`
cuisine_filter | List of Integers | A list of integers coresponding to cuisine types in the Relationships and Restaurants database | `[1,2,etc]`
price_filter | List of Integers | A list of integers coresponding to price ratings in the Restaurants database| `[1,2,etc]`
duck_bux_filter | Boolean | A Boolean to value screen restaurants against | `True`
meal_points_filter | Boolean | A Boolean to value screen restaurants against | `True`
hours_filter | Boolean | A Boolean value to screen restaurants against | `True`
restaurant_dictionary_list | List of Dictionaries | A list of dictionaries whos value correspond to formated database query results | `[{'name': 'Panda Express',etc},{etc},etc]`
restaurant_ids | List of Integers | A list of integers whos values coresponde to Restaurant_id in the Restaurants database | `[1,2,etc]`
restaurants_list | List of SQLAlchemy Restaurant instance variables | The restaurant_list is used to move SQLAlchemy instance variable query results through a workflow where each instance is further filterd and formatted | `[<RESTAURANT:>,etc]`
hours_query | List of SQLAlchemy Hours instance variables | The list of Hours variables represent all hours of operation of a single restaurant in the Restaurants database | `[<67 0 '11:00' '00:00'>,etc]`
military_time_string | String | A string whos value corresponds to Military Time | `20:30`
formated_time_string | String | A string whos value corresponds to 12 hour time | `11:00AM`
cuisines_dict | Dictionary | A dictionary of all cuisines within the restaurants database. <br><br> The keys of the dictionary represent valid arguments for the cuisine_filter | `{1: 'All You Can Eat', 2: 'American',etc}`
prices_list | List of Integers | A list of integers whos values represent all price ratings within the restaurants database. <br><br> The values of the list represent valid arguments for the price_filter | `[1,2,etc]`
cuisines_list | List of Integers | A list of integers whos values represent all cuisine types within the Cuisines database |`[1,2,etc]`