import pytest

from perivale import Buffer
from perivale.helpers import parse_integer, integer_present


def test_integer_present():
    
    assert integer_present(Buffer("1234567890"), 10)
    assert integer_present(Buffer("09afAF"), 16)
    assert integer_present(Buffer("012345678"), 8)
    assert integer_present(Buffer("01"), 2)

    assert not integer_present(Buffer(""))
    assert not integer_present(Buffer("lorem ipsum dolor"))


def test_parse_integer_valid():

    # Decimal
    for text in ["0", "2", "1024"]:
        buffer = Buffer(text)
        assert parse_integer(buffer, consume=True) == int(text)
        assert buffer.finished()
    
    # Binary
    assert parse_integer(Buffer("100"), base=2) == int("100", 2)
    
    # Hexadecimal
    assert parse_integer(Buffer("09afAF"), base=16) == int("09afAF", 16)

    # Octal
    assert parse_integer(Buffer("07"), base=8) == int("07", 8)


def test_parse_integer_invalid():

    # No integer present
    with pytest.raises(Exception):
        parse_integer(Buffer(""))
    
    # Unsupported base
    with pytest.raises(Exception):
        parse_integer(Buffer(""), base=12)
    