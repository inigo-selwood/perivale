import pytest

from perivale import Buffer
from perivale.helpers import parse_escape_code


def test_parse_escape_code_valid():

    escape_codes = {
        "\\'": "'",
        "\\\"": "\"",
        "\\\\": "\\",

        "\\n": "\n",
        "\\t": "\t",
        "\\r": "\r",
    }

    for symbol, code in escape_codes.items():
        buffer = Buffer(symbol)
        assert parse_escape_code(buffer, 
                escape_codes, 
                [], 
                consume=True) == code
        assert buffer.finished()
    

def test_parse_escape_code_invalid():

    # No backslash found
    with pytest.raises(Exception):
        parse_escape_code(Buffer(""), {})
    
    # Empty symbol
    with pytest.raises(ValueError):
        parse_escape_code(Buffer(""), {"": ""})
    
    # Duplicate symbol
    with pytest.raises(ValueError):
        escape_codes = {
            "\\n": "\n",
            "n": "\n",
        }
        parse_escape_code(Buffer(""), escape_codes)
    
    escape_codes = {
        "\\'": "'",
        "\\\"": "\"",
        "\\\\": "\\",

        "\\n": "\n",
        "\\t": "\t",
        "\\r": "\r",
    }

    # Incomplete code
    errors = []
    assert not parse_escape_code(Buffer("\\"), escape_codes, errors)
    message, excerpt = errors[0].excerpts[0]
    assert message == "incomplete escape code"
    assert excerpt.position.line == 1
    assert excerpt.position.column == 1

    # Invalid code
    errors = []
    assert not parse_escape_code(Buffer("\\@"), escape_codes, errors)
    message, excerpt = errors[0].excerpts[0]
    assert message == "invalid escape code"
    assert excerpt.position.line == 1
    assert excerpt.position.column == 1