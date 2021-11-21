from trio_websocket import serve_websocket, ConnectionClosed
from functools import partial
import trio
import json
import pprint


# BUSES_DATABASE - имитация базы данных с автобусами, их текущими координатами
# и номером марщрута.
# Структура:
#         {
#             busId: {
#             lat: lat,
#             lng: lng,
#             route: route,
#             }
#         }
BUSES_DATABASE = {}


def update_buses_database(bus_routing_info):
    bus_id = bus_routing_info['busId']
    lat, lng = bus_routing_info['lat'], bus_routing_info['lng']
    route = bus_routing_info['route']
    if not BUSES_DATABASE.get(bus_id):
        BUSES_DATABASE.update({
            bus_id: {
                'lat': lat,
                'lng': lng,
                'route': route,
            }
        })
    else:
        BUSES_DATABASE[bus_id]['lat'] = bus_routing_info['lat']
        BUSES_DATABASE[bus_id]['lng'] = bus_routing_info['lng']


def get_info_from_database():
    routing_info = [
        {
            'busId': key,
            'lat': value['lat'],
            'lng': value['lng'],
            'route': value['route'],
        }
        for key, value in BUSES_DATABASE.items()
    ]
    return {'msgType': 'Buses', 'buses': routing_info}


async def talk_to_browser(request):
    ws = await request.accept()
    while True:
        current_routing_info = get_info_from_database()
        try:
            await ws.send_message(json.dumps(current_routing_info))
        except ConnectionClosed:
            break

        await trio.sleep(1)


async def get_routing_info(request):
    ws = await request.accept()
    while True:
            try:
                bus_routing_info = await ws.get_message()
            except ConnectionClosed:
                break

            update_buses_database(json.loads(bus_routing_info))


async def main():
    recipient_info = partial(serve_websocket, get_routing_info, '127.0.0.1', 8080, ssl_context=None)
    sender_info = partial(serve_websocket, talk_to_browser, '127.0.0.1', 8000, ssl_context=None)
    async with trio.open_nursery() as nursery:
        nursery.start_soon(sender_info)
        nursery.start_soon(recipient_info)


if __name__ == '__main__':
    try:
        trio.run(main)
    except KeyboardInterrupt:
        print('Server stopped.')
