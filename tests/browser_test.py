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
    value = browser_validator(json.dumps(msg))
    assert value == msg


def test_not_json():
    msg = 'some string'
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        browser_validator(msg)


def test_not_valid_json():
    msg = {"a": 123, "b": 456}
    with pytest.raises(MessageErrors, match='Requires msgType specified'):
        browser_validator(json.dumps(msg))


def test_no_msgtype():
    msg = {
        "data": {
            "east_lng": 37.65563964843751,
            "north_lat": 55.77367652953477,
            "south_lat": 55.72628839374007,
            "west_lng": 37.54440307617188,
        }
    }
    with pytest.raises(MessageErrors, match='Requires msgType specified'):
        browser_validator(json.dumps(msg))


def test_no_data():
    msg = {
        "msgType": "newBounds"
    }
    with pytest.raises(MessageErrors, match='Requires data specified'):
        browser_validator(json.dumps(msg))


def test_not_correct_data():
    msg = {
        "msgType": "newBounds",
        "data": [
            37.65563964843751,
            55.77367652953477,
            55.72628839374007,
            37.54440307617188,
        ],
    }
    with pytest.raises(MessageErrors, match='Requires data specified'):
        browser_validator(json.dumps(msg))


def test_no_west_lng():
    msg = {
        "msgType": "newBounds",
        "data": {
            "east_lng": 37.65563964843751,
            "north_lat": 55.77367652953477,
            "south_lat": 55.72628839374007,
        },
    }
    with pytest.raises(MessageErrors, match='Requires west_lng specified'):
        browser_validator(json.dumps(msg))


def test_not_correct_west_lng():
    msg = {
        "msgType": "newBounds",
        "data": {
            "east_lng": 37.65563964843751,
            "north_lat": 55.77367652953477,
            "south_lat": 55.72628839374007,
            "west_lng": [37.54440307617188],
        },
    }
    with pytest.raises(MessageErrors, match='Requires west_lng specified'):
        browser_validator(json.dumps(msg))


def test_no_east_lng():
    msg = {
        "msgType": "newBounds",
        "data": {
            "north_lat": 55.77367652953477,
            "south_lat": 55.72628839374007,
            "west_lng": 37.54440307617188,
        },
    }
    with pytest.raises(MessageErrors, match='Requires east_lng specified'):
        browser_validator(json.dumps(msg))


def test_not_correct_east_lng():
    msg = {
        "msgType": "newBounds",
        "data": {
            "east_lng": "37.65563964843751",
            "north_lat": 55.77367652953477,
            "south_lat": 55.72628839374007,
            "west_lng": 37.54440307617188,
        },
    }
    with pytest.raises(MessageErrors, match='Requires east_lng specified'):
        browser_validator(json.dumps(msg))


def test_no_north_lat():
    msg = {
        "msgType": "newBounds",
        "data": {
            "east_lng": 37.65563964843751,
            "south_lat": 55.72628839374007,
            "west_lng": 37.54440307617188,
        },
    }
    with pytest.raises(MessageErrors, match='Requires north_lat specified'):
        browser_validator(json.dumps(msg))


def test_not_correct_north_lat():
    msg = {
        "msgType": "newBounds",
        "data": {
            "east_lng": 37.65563964843751,
            "north_lat": {"north_lat": 55.77367652953477},
            "south_lat": 55.72628839374007,
            "west_lng": 37.54440307617188,
        },
    }
    with pytest.raises(MessageErrors, match='Requires north_lat specified'):
        browser_validator(json.dumps(msg))


def test_no_south_lat():
    msg = {
        "msgType": "newBounds",
        "data": {
            "east_lng": 37.65563964843751,
            "north_lat": 37.54440307617188,
            "west_lng": 37.54440307617188,
        },
    }
    with pytest.raises(MessageErrors, match='Requires south_lat specified'):
        browser_validator(json.dumps(msg))


def test_not_correct_south_lat():
    msg = {
        "msgType": "newBounds",
        "data": {
            "east_lng": 37.65563964843751,
            "north_lat": 55.72628839374007,
            "south_lat": None,
            "west_lng": 37.54440307617188,
        },
    }
    with pytest.raises(MessageErrors, match='Requires south_lat specified'):
        browser_validator(json.dumps(msg))
