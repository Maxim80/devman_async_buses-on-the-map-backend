from sys import stderr
from trio_websocket import open_websocket_url
import trio
import json
import os


def load_routes(directory_path='routes'):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r', encoding='utf8') as file:
                yield json.load(file)


async def run_bus(url, bus_id, route):
    message = {
        'busId': bus_id,
        'lat': None,
        'lng': None,
        'route': route['name'],
    }
    try:
        async with open_websocket_url(f'ws://{url}') as ws:
            for lat, lng in route['coordinates']:
                message['lat'] = lat
                message['lng'] = lng
                await ws.send_message(json.dumps(message, ensure_ascii=False))
                await trio.sleep(1)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)


async def main():
    async with trio.open_nursery() as nursery:
        for route in load_routes():
            nursery.start_soon(run_bus, '127.0.0.1:8080', route['name'], route)


if __name__ == '__main__':
    try:
        trio.run(main)
    except trio_websocket._impl.ConnectionClosed:
        print('Connection closed')

"""
{
    "busId": "c790сс",
    "lat": 55.747629944737,
    "lng": 37.641726387317,
    "route": "156"
}
"""
