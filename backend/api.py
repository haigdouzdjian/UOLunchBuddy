'''
Implementation of the API used for UO Lunch Buddy
'''

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Cross-Origin-Resource-Sharing
from app import App
import json
from utils import *
api = Flask(__name__)
CORS(api)
app = App(api)


def make_json(code=0, message='success', data={}):
    obj = {
        'code': code,
        'message': message}
    for key, value in data.items():
        obj[key] = value
    return obj


def make_geojson(data):
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }
    for restaurant in data:
        coords = restaurant.get('coordinates').split(',')
        # Swap to get the correct lat, lon position
        coords[0], coords[1] = coords[1], coords[0]
        del restaurant['coordinates']
        obj = {
            'type': 'Feature',
            'properties': restaurant,
            'geometry': {
                'type': 'Point',
                'coordinates': coords
            }
        }
        geojson['features'].append(obj)
    return geojson


@api.route('/', methods=['GET'])
def test_route():
    msg = make_json(code=0, message='API is working.', data={})
    msg = jsonify(msg)
    msg.status_code = 200
    return msg


@api.route('/cuisines', methods=['GET'])
def get_cuisines():
    (code, resp) = app.get_cuisines()
    if code == 0:
        cuisines_list = []
        for key, value in resp.items():
            cuisines_list.append([key, value])
        return jsonify(
            make_json(
                code=0,
                message='success',
                data={
                    'cuisines': cuisines_list}))
    else:
        return jsonify(make_json(code, 'error retrieving cuisines', data))


@api.route('/restaurants', methods=['GET', 'POST'])
def get_restaurants():
    # Try to convert the request's payload to JSON
    # If unsuccessful, it is an invalid request
    try:
        data = request.json
        if data is None:
            raise Exception
    except BaseException:
        data = {}

    # Get each of the filters from the payload
    cuisine_filter = data.get('cuisines')
    price_filter = data.get('prices')
    duck_bux_filter = data.get('duck_bux')
    meal_points_filter = data.get('meal_points')

    if cuisine_filter is not None:
        for item in cuisine_filter:
            try:
                item = int(item)
            except BaseException:
                return jsonify(
                    make_json(
                        2, 'cuisine filter has a non-integer'))
            if item < 1:
                return jsonify(
                    make_json(
                        2, 'cuisine filter has a non-positive integer'))

    if price_filter is not None:
        for item in price_filter:
            try:
                item = int(item)
            except BaseException:
                return jsonify(make_json(3, 'price filter has a non-integer'))
            if item < 1 or item > 5:
                return jsonify(
                    make_json(
                        3,
                        'price filter has an integer not in the range: [1-5]'))

    if duck_bux_filter is not None:
        if str(duck_bux_filter) != 'True' and str(duck_bux_filter) != 'False':
            return jsonify(
                make_json(
                    4, 'duck_bux filter is not a boolean value'))

    if meal_points_filter is not None:
        if str(meal_points_filter) != 'True' and str(
                meal_points_filter) != 'False':
            return jsonify(
                make_json(
                    5, 'meal_points filter is not a boolean value'))

    code, restaurants = app.get_restaurants(
        cuisine_filter, price_filter, duck_bux_filter, meal_points_filter)
    if code == 0:
        message = 'success'
    else:
        message = 'best-fit'
    json_response = make_json(
        code, message, {
            'restaurants': make_geojson(restaurants)})
    return jsonify(json_response)


@api.route('/submission', methods=['POST'])
def submission_post():
    # TODO: figure out error codes
    # TODO: make sure return is JSON
    if request.method != 'POST':
        return jsonify(make_json(1, 'method is not POST'))

    if request.form is None:
        return jsonify(make_json(2, 'no form found to parse'))

    email = request.form.get('email')
    comment = request.form.get('comment')

    if email is None:
        email = ''

    if comment is None or comment == '':
        return jsonify(2, 'comment cannot be empty')

    app.handle_submission(email, comment)
    return jsonify(make_json())


@api.route('/submissions', methods=['GET'])
def get_submissions():
    submissions = app.get_submissions()
    return render_template('submissions.html', submissions=submissions)


if __name__ == "__main__":
    setup_log()
    api.run(host='localhost', port=3600, debug=True)
