import pytest

from perivale import Buffer
from perivale.helpers import parse_identifier


def test_parse_identifier_valid():

    assert parse_identifier(Buffer("_azAZ09")) == "_azAZ09"
    assert parse_identifier(Buffer("_azAZ09+-")) == "_azAZ09"


def test_parse_identifier_invalid():

    # No identifier present
    with pytest.raises(Exception):
        parse_identifier(Buffer(""))
    