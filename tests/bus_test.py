from validators import bus_validator
from validators import MessageErrors
import pytest
import json


def test_correct_json():
    msg = {"busId": "c790сс", "lat": 55.7500, "lng": 37.600, "route": "120"}
    value = bus_validator(json.dumps(msg))
    assert value == msg


def test_not_json():
    msg = 'some string'
    with pytest.raises(MessageErrors, match='Requires valid JSON'):
        bus_validator(msg)


def test_not_valid_json():
    msg = {"a": 123, "b": 456}
    with pytest.raises(MessageErrors, match='Requires busId specified'):
        bus_validator(json.dumps(msg))


def test_no_busid():
    msg = {"lat": 55.7500, "lng": 37.600, "route": "120"}
    with pytest.raises(MessageErrors, match='Requires busId specified'):
        bus_validator(json.dumps(msg))


def test_not_correct_busid():
    msg = {"busId": ['a', 1], "lat": 55.7500, "lng": 37.600, "route": "120"}
    with pytest.raises(MessageErrors, match='Requires busId specified'):
        bus_validator(json.dumps(msg))


def test_no_lat():
    msg = {"busId": "c790сс", "lng": 37.600, "route": "120"}
    with pytest.raises(MessageErrors, match='Requires lat specified'):
        bus_validator(json.dumps(msg))


def test_not_correct_lat():
    msg = {"busId": "c790сс", "lat": "55.7500", "lng": 37.600, "route": "120"}
    with pytest.raises(MessageErrors, match='Requires lat specified'):
        bus_validator(json.dumps(msg))


def test_no_lng():
    msg = {"busId": "c790сс", "lat": 55.7500, "route": "120"}
    with pytest.raises(MessageErrors, match='Requires lng specified'):
        bus_validator(json.dumps(msg))


def test_not_correct_lng():
    msg = {"busId": "c790сс", "lat": 55.7500, "lng": "37.600", "route": "120"}
    with pytest.raises(MessageErrors, match='Requires lng specified'):
        bus_validator(json.dumps(msg))


def test_no_route():
    msg = {"busId": "c790сс", "lat": 55.7500, "lng": 37.600}
    with pytest.raises(MessageErrors, match='Requires route specified'):
        bus_validator(json.dumps(msg))


def test_not_correct_route():
    msg = {"busId": "c790сс", "lat": 55.7500, "lng": 37.600, "route": 1111}
    with pytest.raises(MessageErrors, match='Requires route specified'):
        bus_validator(json.dumps(msg))
