import pytest
from can_parser_v2 import CANparser

def test_speed_below_limit():
    parser = CANparser("can_log.asc")
    result = parser.validate("Vehicle Speed", 199)
    assert result == "PASS"


def test_speed_at_limit():
    parser = CANparser("can_log.asc")
    result = parser.validate("Vehicle Speed", 200)
    assert result == "PASS"


def test_speed_above_limit():
    parser = CANparser("can_log.asc")
    result = parser.validate("Vehicle Speed", 201)
    assert result == "FAIL"

def test_unknown_signal():
    parser = CANparser("can_log.asc")
    result = parser.validate("Battery Voltage", 12)
    assert result == "UNKNOWN"

def test_decode_signal():
    parser = CANparser("can_log.asc")
    result = parser.decode_signal("0A0", ["C9"])
    assert result == ("Vehicle Speed", 201, "km/h")

def test_decode_engine_speed():
    parser = CANparser("can_log.asc")
    result = parser.decode_signal("0C8", ["64"])
    assert result == ("Engine Speed", 3000, "RPM")


def test_empty_data():
    parser = CANparser("can_log.asc")
    
    with pytest.raises(ValueError):
        parser.decode_signal("0A0", [])


def test_invalid_hex_data():
    parser = CANparser("can_log.asc")

    with pytest.raises(ValueError):
        parser.decode_signal("0A0", ["ZZ"])