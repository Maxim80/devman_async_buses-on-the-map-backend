from trio_websocket import serve_websocket, ConnectionClosed
import trio
import json


test_msg = {
  "msgType": "Buses",
  "buses": [
    {"busId": "c790сс", "lat": 55.750342, "lng": 37.624202, "route": "120"},
    {"busId": "a134aa", "lat": 55.748291, "lng": 37.620695, "route": "670к"},
  ]
}



async def echo_server(request):
    ws = await request.accept()
    while True:
        try:
            message = await ws.get_message()
            await ws.send_message(json.dumps(test_msg))
        except ConnectionClosed:
            break


async def main():
    await serve_websocket(echo_server, '127.0.0.1', 8000, ssl_context=None)


if __name__ == '__main__':
    trio.run(main)
