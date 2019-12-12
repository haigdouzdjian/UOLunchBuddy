# UO Lunch Buddy

Table of Contents

+ [API](#api)
  + [/cuisines](#cuisines)
  + [/restaurants](#restaurants)
  + [restaurant Object](#restaurant-object)


## API

This document outlines the API (Application Programming Interface) used by
*UO Lunch Buddy*. It documents the API endpoints, what the expected input is
and what the expected output is.

Because the API will be part of the backend, and not publicly-accessible, it will be
run on localhost:3600.

All data passed to and from the API will be compliant with the JSON data format. See [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259.txt)
for more information.


---

### `/cuisines`
This endpoint allows the frontend to get a list of known cuisines from the database

#### Request Format
No format, just an empty JSON object

#### Example Request
```JSON
{}
```

#### Resonse Format

Name | Type | Description
-----|------|------------
cuisines | JSON object | The map of cuisine IDs to cuisine strings

#### Response Codes
Code | Message | Description
-----|---------|------------
0 | "success" | This code is returned on the successful processing of a request

#### Example Response
```JSON
{
    "cuisines": {
        "0": "American",
        "1": "Smoothie",
        "2": "Bowl",
        "3": "Snack"
    }
}
```
---

### `/restaurants`
This endpoint allows a user to request a list of known restaurants from the database.

#### Request Format
None of the following fields are required. In the event that the requested filter yields
an empty set of restaurants, a "best-match" is returned instead

Name | Type | Description | Remarks
-----|------|-------------|--------
cuisines | list of integers | Filter: any restaurants matching a cusinine ID found in this field will be included. Non-matches will be excluded | If an empty list is passed, the filter is ignored
prices | list of integers | Filter: any restaurants matching a price point associated with a value in the list will be included in the response. Non-matches will be excluded | If an empty list is passed, the filter is ignored
duck_bux | boolean | Filter: any restaurants matching the boolean value for duck_bux will be included in the response. Non-matches will be excluded. | If the key is not passed, or the value is None, the filter is ignored
meal_points | boolean | Filter: any restaurants matching the boolean value for meal_points will be included in the response. Non-matches will be excluded. | If the key is not passed, or the value is None, the filter is ignored

#### Example Request
```JSON
{
    "cuisines": [0, 4, 7, 10],
    "prices": [1, 2]
}
```

#### Response Format
Name | Type | Description | Remarks
-----|------|-------------|--------
code | integer | An integer code noting the success or failure of the request | Any non-zero code indicates failure
message | string | A string indicating the success or failure of the request | In the event of a code: 0, this field can safely be ignored. It is recommended to log the value of this field in some way in the event of a non-zero code
restaurants | list of restaurant objects in GeoJSON format | The "payload" of the response. This is the list of restaurants generated by the request, with filters appropriately applied. | If a filter yielded an empty set of restaurants, a 'best-match' list of restaurants will be returned

#### Response Codes
Code | Message | Notes
-----|---------|------
0 | "success" | This code is returned on the successful processing of a request
1 | "best-match" | This code is returned in the event that the filter(s) did not match any restaurants. Thus, a best match has been returned.
2 | "cuisine filter [error]" | This code is returned when there is an issue with the cuisine filter
3 | "price filter [error]" | This code is returned when there is an issue with the price filter
4 | "duck_bux filter is not a boolean value" | This code is returned when the duck_bux filter is not a boolean
5 | "meal_points filter is not a boolean value" | This code is returned when the meal_points filter is not a boolean


#### Example Response
```JSON
{
    "code": 0,
    "message": "success",
    "restaurants": {
        "type": "FeatureCollector",
        "features": [
            {
                "geometry": {
                    "coordinates": [
                        "44.048839",
                        "-123.084284"
                    ],
                    "type": "Point"
                },
                "properties": {
                    "cuisines": [
                        "All You Can Eat"
                    ],
                    "duck_bux": 1,
                    "hours": "Monday: 11:00AM -  4:30PM,  5:00PM -  8:00PM\nTuesday: 11:00AM -  4:30PM,  5:00PM -  8:00PM\nWednesday: 11:00AM -  4:30PM,  5:00PM -  8:00PM\nThursday: 11:00AM -  4:30PM,  5:00PM -  8:00PM\nFriday: 11:00AM -  4:30PM,  5:00PM -  8:00PM\nSaturday:  9:00AM -  8:00PM\nSunday:  9:00AM -  8:00PM",
                    "location": "Barnhart Hall",
                    "meal_points": 1,
                    "name": "Barnhart Dining",
                    "price": 1,
                    "restaurant_id": 1
                },
                "type": "Feature"
            }
        ]
    }
}
```

---

### `restaurant` Object

There is one significant custom data type: `restaurant`

Name | Type | Description
-----|------|------------
name | string | The name of the restaurant
cuisines | list of strings | The cuisine types associated with the restaurant
coordinates | string | The latitude and longitude of the restaurant. Comma-Separated Values, latitude first
location | string | Address of the restaurant
duck_bux | boolean | Whether the restaurant accepts Duck Bux
meal_points | boolean | Whether the restaurant accepts meal points
hours | string | The hours of operation of the restaurant
price | integer | The price "category" of the restaurant. Ranges from 1-5, inclusive