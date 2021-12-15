from sys import stderr
from trio_websocket import open_websocket_url
from itertools import cycle, islice
import asyncclick as click
import trio
import json
import os
import random


def generate_bus_id(route_id, bus_index):
    return f"{route_id}-{bus_index}"


def load_routes(directory_path='routes'):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf8') as file:
                yield json.load(file)


async def send_updates(server_address, receive_channel):
    async with open_websocket_url(f'ws://{server_address}') as ws:
        async for bus_routing_info in receive_channel:
            try:
                await ws.send_message(json.dumps(bus_routing_info, ensure_ascii=False))

            except OSError as ose:
                print('Connection attempt failed: %s' % ose, file=stderr)


async def run_bus(send_channel, bus_index, route, delay):
    bus_routing_info = {
        'busId': generate_bus_id(route['name'], bus_index),
        'lat': None,
        'lng': None,
        'route': route['name'],
    }
    start_coordinate = random.randint(0, len(route['coordinates']))
    coordinates = route['coordinates'][start_coordinate:] + route['coordinates'][:start_coordinate]
    for lat, lng in cycle(coordinates):
        bus_routing_info['lat'], bus_routing_info['lng'] = lat, lng
        await send_channel.send(bus_routing_info)
        await trio.sleep(delay)


@click.command()
@click.option('-s', '--server', default='127.0.0.1:8080', help='Server address')
@click.option('-rn', '--routes_number', default=100, help='Routes number')
@click.option('-bpr', '--buses_per_route', default=5, help='Number of buses on the route')
@click.option('-wn', '--websockets_number', default=10, help='Number of open web sockets')
@click.option('-ei', '--emulator_id', default='00a', help='BusId prefix in case of running multiple instances of the simulator')
@click.option('-rt', '--refresh_timeout', default=0.3, help='Delay in updating coordinates')
@click.option('-v', '--verbose', default=False, help='Enable logging')
async def main(**kwargs):
    channels = [trio.open_memory_channel(0) for _ in range(0, kwargs['websockets_number'])]
    async with trio.open_nursery() as nursery:
        for _, receive_channel in channels:
            nursery.start_soon(send_updates, kwargs['server'], receive_channel)

        for route in islice(load_routes(), kwargs['routes_number']):
            for index in range(kwargs['buses_per_route']):
                bus_index = f"{kwargs['emulator_id']}{index}"
                send_channel, _ = random.choice(channels)
                nursery.start_soon(run_bus, send_channel, bus_index, route, kwargs['refresh_timeout'])


if __name__ == '__main__':
    main(_anyio_backend="trio")
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
