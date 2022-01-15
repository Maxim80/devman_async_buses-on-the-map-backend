import json


class MessageErrors(Exception):
    pass


def browser_validator(msg):
    try:
        msg = json.loads(msg)
    except json.decoder.JSONDecodeError:
        raise MessageErrors('Requires valid JSON')

    msg_keys = msg.keys()
    if msg_keys != {'msgType', 'data'}:
        raise MessageErrors('Requires valid JSON')

    if msg['msgType'] != 'newBounds':
        raise MessageErrors('Requires msgType specified')

    if type(msg['data']) != dict:
        raise MessageErrors('Requires valid JSON')

    if msg['data'].keys() != {'west_lng', 'east_lng', 'north_lat', 'south_lat'}:
        raise MessageErrors('Requires valid JSON')

    return msg
