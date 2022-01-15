import json


class MessageErrors(Exception):
    pass


def browser_validator(msg):
    try:
        msg = json.loads(msg)
    except json.decoder.JSONDecodeError:
        raise MessageErrors('Requires valid JSON')

    msg_type = msg.get('msgType')
    if not msg_type or msg_type != 'newBounds':
        raise MessageErrors('Requires msgType specified')

    data = msg.get('data')
    if not data or type(data) != dict:
        raise MessageErrors('Requires data specified')

    west_lng = data.get('west_lng')
    if not west_lng or type(west_lng) != float:
        raise MessageErrors('Requires west_lng specified')

    east_lng = data.get('east_lng')
    if not east_lng or type(east_lng) != float:
        raise MessageErrors('Requires east_lng specified')

    north_lat = data.get('north_lat')
    if not north_lat or type(north_lat) != float:
        raise MessageErrors('Requires north_lat specified')

    south_lat = data.get('south_lat')
    if not south_lat or type(south_lat) != float:
        raise MessageErrors('Requires south_lat specified')

    return msg


def bus_validator(msg):
    try:
        msg = json.loads(msg)
    except json.decoder.JSONDecodeError:
        raise MessageErrors('Requires valid JSON')

    bus_id = msg.get('busId')
    if not bus_id or type(bus_id) != str:
        raise MessageErrors('Requires busId specified')

    lat = msg.get('lat')
    if not lat or type(lat) != float:
        raise MessageErrors('Requires lat specified')

    lng = msg.get('lng')
    if not lng or type(lng) != float:
        raise MessageErrors('Requires lng specified')

    route = msg.get('route')
    if not route or type(route) != str:
        raise MessageErrors('Requires route specified')

    return msg
