import pytest

from perivale import Buffer
from perivale.helpers import parse_identifier, identifier_present


def test_identifier_present():
    assert identifier_present(Buffer("_azAZ09"))
    assert not identifier_present(Buffer("09_azAZ"))


def test_parse_identifier_valid():

    assert parse_identifier(Buffer("_azAZ09")) == "_azAZ09"
    assert parse_identifier(Buffer("_azAZ09+-")) == "_azAZ09"


def test_parse_identifier_invalid():

    # No identifier present
    with pytest.raises(Exception):
        parse_identifier(Buffer(""))
    