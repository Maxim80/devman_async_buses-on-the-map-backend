from trio_websocket import open_websocket_url
from itertools import cycle, islice
from contextlib import suppress
import trio_websocket
import asyncclick as click
import trio
import json
import os
import random
import logging


def get_logger(name):
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger


def relaunch_on_disconnect(func):
    async def wrapped(*args, **kwargs):
        while True:
            try:
                await func(*args, **kwargs)
            except (trio_websocket._impl.HandshakeError,
                    trio_websocket._impl.ConnectionClosed):
                logger.debug('Нет подключения')
                await trio.sleep(1)
                continue

    return wrapped


def generate_bus_id(route_id, bus_index):
    return f"{bus_index}-{route_id}"


def load_routes(directory_path='routes'):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf8') as file:
                yield json.load(file)


@relaunch_on_disconnect
async def send_updates(server_address, receive_channel):
    async with open_websocket_url(f'ws://{server_address}') as ws:
        logger.debug('Подключение установлено')
        async for bus_routing_info in receive_channel:
            await ws.send_message(
                json.dumps(bus_routing_info, ensure_ascii=False))



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
@click.option('--server', default='127.0.0.1:8080', help='Server address')
@click.option('--routes_number', default=20, help='Routes number')
@click.option('--buses_per_route', default=2,
    help='Number of buses on the route')
@click.option('--websockets_number', default=10,
    help='Number of open web sockets')
@click.option('--emulator_id', default='00a',
    help='BusId prefix in case of running multiple instances of the simulator')
@click.option('--refresh_timeout', default=0.3,
    help='Delay in updating coordinates')
@click.option('--debug/--no-debug', default=False, help='Enable logging')
async def main(**kwargs):
    logger.disabled = not kwargs['debug']
    channels = [
        trio.open_memory_channel(0)
        for _ in range(0, kwargs['websockets_number'])
    ]
    async with trio.open_nursery() as nursery:
        for _, receive_channel in channels:
            nursery.start_soon(send_updates, kwargs['server'], receive_channel)

        for route in islice(load_routes(), kwargs['routes_number']):
            for index in range(kwargs['buses_per_route']):
                bus_index = f"{kwargs['emulator_id']}{index}"
                send_channel, _ = random.choice(channels)
                nursery.start_soon(run_bus, send_channel, bus_index, route,
                    kwargs['refresh_timeout'])


if __name__ == '__main__':
    logger = get_logger('FAKE_BUS')

    with suppress(KeyboardInterrupt):
        main(_anyio_backend="trio")
