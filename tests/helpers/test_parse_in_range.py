import pytest

from perivale.helpers import in_range


def test_parse_in_range_valid():

    assert in_range("a", "a", "z")
    assert not in_range("A", "a", "z")


def test_parse_range_invalid():

    with pytest.raises(ValueError):
        in_range("a", "z", "a")