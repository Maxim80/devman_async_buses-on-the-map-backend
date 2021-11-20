from sys import stderr
from trio_websocket import open_websocket_url
import trio
import json


async def main():
    message = {
        "busId": "c790сс",
        "lat": 55.747629944737,
        "lng": 37.641726387317,
        "route": "156"
    }
    try:
        async with open_websocket_url('ws://127.0.0.1:8000') as ws:
            await ws.send_message(json.dumps(message))
            # message = await ws.get_message()
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)

trio.run(main)
