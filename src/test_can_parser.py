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