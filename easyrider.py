import json
import re

# data = [
#     {
#         "bus_id": 128,
#         "stop_id": 1,
#         "stop_name": "Prospekt Avenue",
#         "next_stop": 3,
#         "stop_type": "S",
#         "a_time": "08:12"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 3,
#         "stop_name": "Elm Street",
#         "next_stop": 5,
#         "stop_type": "",
#         "a_time": "08:19"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 5,
#         "stop_name": "Fifth Avenue",
#         "next_stop": 7,
#         "stop_type": "O",
#         "a_time": "08:25"
#     },
#     {
#         "bus_id": 128,
#         "stop_id": 7,
#         "stop_name": "Sesame Street",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:37"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 2,
#         "stop_name": "Pilotow Street",
#         "next_stop": 3,
#         "stop_type": "S",
#         "a_time": "09:20"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 3,
#         "stop_name": "Elm Street",
#         "next_stop": 6,
#         "stop_type": "",
#         "a_time": "09:45"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 7,
#         "stop_type": "",
#         "a_time": "09:59"
#     },
#     {
#         "bus_id": 256,
#         "stop_id": 7,
#         "stop_name": "Sesame Street",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "10:12"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 4,
#         "stop_name": "Bourbon Street",
#         "next_stop": 6,
#         "stop_type": "S",
#         "a_time": "08:13"
#     },
#     {
#         "bus_id": 512,
#         "stop_id": 6,
#         "stop_name": "Sunset Boulevard",
#         "next_stop": 0,
#         "stop_type": "F",
#         "a_time": "08:16"
#     }
# ]

stop_ids = [
    'Prospekt Avenue',
    'Pilotow Street',
    'Elm Street',
    'Bourbon Street',
    'Fifth Avenue',
    'Sunset Boulevard',
    'Sesame Street'
]

line_128 = [1, 3, 6, 7]
line_256 = [2, 3, 5, 7]
line_512 = [4, 6]


def check_time(time_string):
    return re.match(r'^([01]\d)?(2\d)?:[0-5]\d$', time_string) is None


def check_stop_name(stop_name):
    return re.match(r'^[A-Z]\w* ([A-Z]\w*)? ?(Road|Avenue|Boulevard|Street)$', stop_name) is None


def stop_bus_lines(stops):
    stop_data = {}
    for stop in stops:
        for key, value in stop.items():
            if key == 'bus_id':
                if value in stop_data:
                    stop_data[value] += 1
                else:
                    stop_data[value] = 1
                break
    return stop_data


def check_stop(bus_id, stop_id, stop_name, next_stop, stop_type, a_time):
    error_fields = []

    if not isinstance(bus_id, int):
        error_fields.append('bus_id')

    if not isinstance(stop_id, int):
        error_fields.append('stop_id')

    if not stop_name or not isinstance(stop_name, str) or check_stop_name(stop_name):
        error_fields.append('stop_name')
        print(stop_name)

    if not isinstance(next_stop, int):
        error_fields.append('next_stop')

    if not isinstance(stop_type, str) or stop_type not in ['S', 'O', 'F', '']:
        error_fields.append('stop_type')

    if not isinstance(a_time, str):
        error_fields.append('a_time')
    else:
        if check_time(a_time):
            error_fields.append("a_time")

    return error_fields


if __name__ == '__main__':
    count = 0
    errors = {
        'bus_id': 0,
        'stop_id': 0,
        'stop_name': 0,
        'next_stop': 0,
        'stop_type': 0,
        'a_time': 0
    }

    # for stop in json.loads(input()):
    #     fields = check_stop(**stop)
    #     for field in fields:
    #         errors[field] += 1
    #         count += 1

    # testing
    # for stop in data:
    #     fields = check_stop(**stop)
    #     for field in fields:
    #         errors[field] += 1
    #         count += 1

    # print(f'Type and required field validation: {count} errors')
    # print(f'stop_name: {errors.get("stop_name")}')
    # print(f'stop_type: {errors.get("stop_type")}')
    # print(f'a_time: {errors.get("a_time")}')

    print('Line names and number of stops:')
    for line, num in stop_bus_lines(json.loads(input())).items():
        print(f'bus_id: {line}, stops: {num}')
