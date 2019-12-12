import requests
import json

failed_tests = {}


def check_response(url, data, code, test, test_name):
    response = json.loads(requests.get(url, json=data).text)
    passed = code == response['code']
    if not passed:
        failed_tests[test] = {'name': test_name, 'code': response['code']}
    print(
        '[{0}] {1}\n    {2}\n'.format(
            test,
            test_name,
            'PASSED' if passed else 'FAILED'))


url_base = 'http://localhost:3600/'

url = url_base + 'restaurants'

data = {}
code = 0
test = 0
test_name = 'empty request'
check_response(url, data, code, test, test_name)

data = {'cuisines': []}
code = 0
test = 1
test_name = 'cuisine: empty list'
check_response(url, data, code, test, test_name)

data = {'cuisines': [1, 2]}
code = 0
test = 2
test_name = 'cuisine: valid filter'
check_response(url, data, code, test, test_name)

data = {'cuisines': [1, 2, 'a']}
code = 2
test = 3
test_name = 'cuisine: non-integers'
check_response(url, data, code, test, test_name)

data = {'cuisines': [1, 2, -1]}
code = 2
test = 4
test_name = 'cuisine: non-positive integers'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': []
}
code = 0
test = 5
test_name = 'price: empty list'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': [1, 2]
}
code = 0
test = 6
test_name = 'price: valid filter'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': [1, 2, 'a']
}
code = 3
test = 7
test_name = 'price: non-integers'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': [1, -2]
}
code = 3
test = 8
test_name = 'price: non-positive integers'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': [1, 2, 6]
}
code = 3
test = 9
test_name = 'price: integer > 5'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': [1, 2],
    'duck_bux': True
}
code = 0
test = 10
test_name = 'duck_bux: valid value'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': [1, 2],
    'duck_bux': 'no'
}
code = 4
test = 11
test_name = 'duck_bux: invalid value'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': [1, 2],
    'duck_bux': True,
    'meal_points': True
}
code = 0
test = 12
test_name = 'meal_points: valid value'
check_response(url, data, code, test, test_name)

data = {
    'cuisines': [1, 2],
    'prices': [1, 2],
    'duck_bux': True,
    'meal_points': 'yes'
}
code = 5
test = 13
test_name = 'meal_points: invalid value'
check_response(url, data, code, test, test_name)


if len(failed_tests) > 0:
    print('\n\nFAILED TESTS')
    print('============\n')
    for failed in failed_tests.values():
        print('{0}\ncode: {1}\n\n'.format(failed['name'], failed['code']))
else:
    print('\n\nALL TESTS PASSED\n\n')
