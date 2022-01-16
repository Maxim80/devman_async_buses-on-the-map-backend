from trio_websocket import serve_websocket, ConnectionClosed
from functools import partial
from contextlib import suppress
from validators import browser_validator, bus_validator, MessageErrors
import asyncclick as click
import trio
import json
import logging
import dataclasses


BUSES_DATABASE = {}


@dataclasses.dataclass
class Bus:
    busId: str
    lat: float
    lng: float
    route: str


@dataclasses.dataclass
class WindowBounds:
    south_lat: float
    north_lat: float
    west_lng: float
    east_lng: float

    def update(self, south_lat, north_lat, west_lng, east_lng):
        self.south_lat = south_lat
        self.north_lat = north_lat
        self.west_lng = west_lng
        self.east_lng = east_lng

    def is_inside(self, lat, lng):
        is_lat = self.south_lat <= lat <= self.north_lat
        is_lng = self.west_lng <= lng <= self.east_lng
        if is_lat and is_lng:
            return True
        else:
            return False


def get_logger(name):
    logging.basicConfig()
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger


async def send_to_browser(ws, bounds):
    while True:
        buses = [
            dataclasses.asdict(bus)
            for bus in BUSES_DATABASE.values()
            if bounds.is_inside(bus.lat, bus.lng)
        ]
        buses_info = {'msgType': 'Buses', 'buses': buses}
        try:
            await ws.send_message(json.dumps(buses_info))
        except ConnectionClosed:
            break

        logger.debug(f'{len(buses)} buses inside bounds')
        await trio.sleep(0.3)


async def read_from_browser(ws, bounds):
    while True:
        try:
            msg = await ws.get_message()
            msg = browser_validator(msg)
        except ConnectionClosed:
            break
        except MessageErrors as err:
            err_msg = {'msgType': 'Errors', 'errors': [str(err)]}
            await ws.send_message(json.dumps(err_msg))
            continue

        bounds.update(**msg['data'])
        logger.debug(msg)


async def talk_to_browser(request):
    ws = await request.accept()
    bounds = WindowBounds(
        **{'south_lat': 0, 'north_lat': 0, 'west_lng': 0, 'east_lng': 0}
    )
    async with trio.open_nursery() as nursery:
        nursery.start_soon(send_to_browser, ws, bounds)
        nursery.start_soon(read_from_browser, ws, bounds)


async def get_bus_info(request):
    ws = await request.accept()
    while True:
        try:
            bus_info = await ws.get_message()
            bus_info = bus_validator(bus_info)
        except ConnectionClosed:
            break
        except MessageErrors as err:
            err_msg = {'msgType': 'Errors', 'errors': [str(err)]}
            await ws.send_message(json.dumps(err_msg))
            continue

        bus = Bus(**bus_info)
        BUSES_DATABASE.update({bus_info['busId']: bus})


@click.command()
@click.option('--bus_port', default=8080, help='Bus port')
@click.option('--browser_port', default=8000, help='Browser port')
@click.option('--debug/--no-debug', default=False, help='Enable logging')
async def main(**kwargs):
    logger.disabled = not kwargs['debug']

    sender = partial(
        serve_websocket,
        talk_to_browser,
        '127.0.0.1', kwargs['browser_port'],
        ssl_context=None)

    receiver = partial(
        serve_websocket,
        get_bus_info,
        '127.0.0.1', kwargs['bus_port'],
        ssl_context=None
    )

    async with trio.open_nursery() as nursery:
        nursery.start_soon(sender)
        nursery.start_soon(receiver)


if __name__ == '__main__':
    logger = get_logger('SERVER')

    with suppress(KeyboardInterrupt):
        main(_anyio_backend="trio")
