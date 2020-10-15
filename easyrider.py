import json
import re
from collections import defaultdict

example_data = [
    {
        "bus_id": 128,
        "stop_id": 1,
        "stop_name": "Prospekt Avenue",
        "next_stop": 3,
        "stop_type": "S",
        "a_time": "08:12"
    },
    {
        "bus_id": 128,
        "stop_id": 3,
        "stop_name": "Elm Street",
        "next_stop": 5,
        "stop_type": "O",
        "a_time": "08:19"
    },
]


def check_time(time_string):
    return re.match(r'^([01]\d)?(2\d)?:[0-5]\d$', time_string) is None


def check_stop_name(stop_name):
    return re.match(r'^[A-Z]\w* ([A-Z]\w*)? ?(Road|Avenue|Boulevard|Street)$', stop_name) is None


def stop_bus_lines(stops):
    stop_data = defaultdict(list)
    for stop in stops:
        for key, value in stop.items():
            if key == 'bus_id':
                stop_data[value].append(stop)
                break
    return stop_data


def check_stop_data(stops):
    result = {
        'start': set(),
        'transfer': defaultdict(list),
        'stop': set(),
        'error': ''
    }
    stop_data = stop_bus_lines(stops)
    for line, stops in stop_data.items():
        start_count = 0
        stop_count = 0
        for stop in stops:
            if stop['stop_type'] == 'S':
                result['start'].add(stop['stop_name'])
                start_count += 1
            elif stop['stop_type'] == 'F':
                result['stop'].add(stop['stop_name'])
                stop_count += 1
            result['transfer'][stop['bus_id']].append(stop['stop_name'])

        if start_count == 0 or start_count > 1 or stop_count == 0 or stop_count > 1:
            result['error'] = f'There is no start or end stop for the line: {stops[0]["bus_id"]}.'
            return result

    intersection_stops = set()
    for i, current_set in enumerate(result['transfer'].values()):
        if i < len(result['transfer']) - 1:
            for j, iter_set in enumerate(result['transfer'].values()):
                if i != j:
                    [intersection_stops.add(value) for value in set(current_set).intersection(set(iter_set))]

    return {
        'Start stops': sorted(result['start']),
        'Transfer stops': sorted(intersection_stops),
        'Finish stops': sorted(result['stop']),
    }


def check_bus_times(stops):
    stop_data = stop_bus_lines(stops)

    time_errors = []

    for bus_stops in stop_data.values():
        curr_time = None
        for bus_stop in bus_stops:
            if not curr_time:
                curr_time = bus_stop['a_time']
            else:
                if curr_time < bus_stop['a_time']:
                    curr_time = bus_stop['a_time']
                else:
                    time_errors.append(
                        f'bus_id line {bus_stop["bus_id"]}: wrong time on station {bus_stop["stop_name"]}')
                    break

    return time_errors


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

    # stage 3
    # print('Line names and number of stops:')
    # for line, num in stop_bus_lines(json.loads(input())).items():
    #     print(f'bus_id: {line}, stops: {num}')

    # stage 4
    # stop_data = check_stop_data(json.loads(input()))
    #
    # if stop_data.get('error'):
    #     print(stop_data['error'])
    # else:
    #     for key, items in stop_data.items():
    #         print(f'{key}: {len(items)} {items}')

    # stage 5
    # time_errors = check_bus_times(json.loads(input()))
    # if time_errors:
    #     print('Arrival time test:')
    #     for error in time_errors:
    #         print(error)
    # else:
    #     print('OK')

    # stage 6
    data = json.loads(input())
    bus_lines = check_stop_data(data)
    on_demand_errors = set()
    for stop in data:
        if stop['stop_type'] == 'O':
            if stop['stop_name'] in bus_lines['Start stops'] or stop['stop_name'] in bus_lines['Transfer stops'] \
                    or stop['stop_name'] in bus_lines['Finish stops']:
                on_demand_errors.add(stop['stop_name'])
    print('On demand stops test:')
    if on_demand_errors:
        print(f'Wrong stop type: {sorted(list(on_demand_errors))}')
    else:
        print('OK')
