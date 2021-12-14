from sys import stderr
from trio_websocket import open_websocket_url
from itertools import cycle, islice
import trio
import json
import os
import random


ROUTE_NUMBER = 10
BUS_NUMBER = 2


def generate_bus_id(route_id, bus_index):
    return f"{route_id}-{bus_index}"


def load_routes(directory_path='routes'):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf8') as file:
                yield json.load(file)


async def run_bus(url, bus_index, route):
    bus_routing_info = {
        'busId': generate_bus_id(route['name'], bus_index),
        'lat': None,
        'lng': None,
        'route': route['name'],
    }
    start_coordinate = random.randint(0, len(route['coordinates']))
    coordinates = route['coordinates'][start_coordinate:] + route['coordinates'][:start_coordinate]
    try:
        async with open_websocket_url(f'ws://{url}') as ws:
            for lat, lng in cycle(coordinates):
                bus_routing_info['lat'], bus_routing_info['lng'] = lat, lng
                await ws.send_message(json.dumps(bus_routing_info, ensure_ascii=False))
                await trio.sleep(0.1)

    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)


async def main():
    async with trio.open_nursery() as nursery:
        for route in islice(load_routes(), ROUTE_NUMBER):
            for index in range(BUS_NUMBER):
                bus_index = f'00{index}'
                nursery.start_soon(run_bus, '127.0.0.1:8080', bus_index, route)


if __name__ == '__main__':
    trio.run(main)
    # try:
    #     trio.run(main)
    # except:
    #     print('Connection closed')

"""
{
    "busId": "c790сс",
    "lat": 55.747629944737,
    "lng": 37.641726387317,
    "route": "156"
}
"""
