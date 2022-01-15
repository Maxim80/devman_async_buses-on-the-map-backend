from validators import browser_validator
from validators import MessageErrors
import pytest
import json


def test_correct_json():
    msg = {
        "msgType": "newBounds",
        "data": {
            "east_lng": 37.65563964843751,
            "north_lat": 55.77367652953477,
            "south_lat": 55.72628839374007,
            "west_lng": 37.54440307617188,
        },
    }
    value = client_validator(json.dumps(msg))
    assert value == msg


def test_not_json_1():
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        msg = 'some string'
        client_validator(msg)


def test_not_json_2():
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        msg = ''
        client_validator(msg)


def test_not_valid_json_1():
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        msg = {"a": 123, "b": 456}
        client_validator(json.dumps(msg))


def test_not_valid_json_2():
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        msg = {
            "msgType": "newBounds",
            "data": {
                "east_lng": 37.65563964843751,
                "north_lat": 55.77367652953477,
                "south_lat": 55.72628839374007,
                "west_lng": 37.54440307617188,
            },
            "data1": {},
        }
        client_validator(json.dumps(msg))

def test_not_valid_json_3():
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        msg = {
            "data": {
                "east_lng": 37.65563964843751,
                "north_lat": 55.77367652953477,
                "south_lat": 55.72628839374007,
                "west_lng": 37.54440307617188,
            },
        }
        client_validator(json.dumps(msg))


def test_not_valid_json_4():
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        msg = {
            "msgType": "newBounds",
            "data": [
                37.65563964843751,
                55.77367652953477,
                55.72628839374007,
                37.54440307617188,
            ],
        }
        client_validator(json.dumps(msg))


def test_not_valid_json_5():
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        msg = {
            "msgType": "newBounds",
            "data": {
                "north_lat": 55.77367652953477,
                "west_lng": 37.54440307617188,
            },
        }
        client_validator(json.dumps(msg))


def test_msgtype_not_specified_1():
    with pytest.raises(MessageErrors, match='Requires msgType specified'):
        msg = {
            "msgType": "",
            "data": {
                "east_lng": 37.65563964843751,
                "north_lat": 55.77367652953477,
                "south_lat": 55.72628839374007,
                "west_lng": 37.54440307617188,
            },
        }
        client_validator(json.dumps(msg))


def test_msgtype_not_specified_2():
    with pytest.raises(MessageErrors, match='Requires msgType specified'):
        msg = {
            "msgType": "someType",
            "data": {
                "east_lng": 37.65563964843751,
                "north_lat": 55.77367652953477,
                "south_lat": 55.72628839374007,
                "west_lng": 37.54440307617188,
            },
        }
        client_validator(json.dumps(msg))
