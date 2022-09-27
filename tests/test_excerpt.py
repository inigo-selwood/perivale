import pytest

from perivale import Buffer, Excerpt, Position


def test_excerpt():

    text = """lorem ipsum
dolor sit amet,
consectetur adipiscing"""
    buffer = Buffer(text)

    # Simple
    excerpt = Excerpt(buffer)
    assert excerpt.__str__() == """[1:1]
    lorem ipsum
    ^"""

    # At position
    position = Position(6, 1, 7)
    excerpt = Excerpt(buffer, position)
    assert excerpt.__str__() == """[1:7]
    lorem ipsum
          ^"""
        
    # At end of line
    position = Position(11, 1, -1)
    excerpt = Excerpt(buffer, position)
    assert excerpt.__str__() == """[1:-1]
    lorem ipsum
               ^"""
    
    # With length
    end = Position(5, 1, 6)
    excerpt = Excerpt(buffer, end=end)
    assert excerpt.__str__() == """[1:1 ... 1:6]
    lorem ipsum
    ^^^^^"""

    # Over two lines
    end = Position(17, 2, 5)
    end.line = 2
    end.column = 6
    excerpt = Excerpt(buffer, end=end)
    assert excerpt.__str__() == """[1:1 ... 2:6]
    lorem ipsum
    ^^^^^^^^^^^
    dolor sit amet,
    ^^^^^"""

    # Over more than two lines
    end = Position(39, 3, 12)
    excerpt = Excerpt(buffer, end=end)
    assert excerpt.__str__() == """[1:1 ... 3:12]
    lorem ipsum
    ^^^^^^^^^^^
    ...
    consectetur adipiscing
    ^^^^^^^^^^^"""

    # Starting at newline (start line should be elided)
    start = Position(11, 1, -1)
    end = Position(17, 2, 6)

    excerpt = Excerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:-1 ... 2:6]
    dolor sit amet,
    ^^^^^"""

    # Ending at newline
    start = Position(0, 1, 1)
    end = Position(11, 1, -1)
    excerpt = Excerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:1 ... 1:-1]
    lorem ipsum
    ^^^^^^^^^^^"""


def test_exception_fail():

    text = """lorem ipsum
dolor sit amet,
consectetur adipiscing"""
    buffer = Buffer(text)

    # Invalid start/end indices
    positions = [
        (0, 0),
        (1, 0),
        (0, 1),

        (1, 12),
        (2, 16),
        (3, 23),

        (4, -1),
    ]

    for start_tuple in positions:
        line, column = start_tuple
        start = Position()
        start.line = line
        start.column = column
        
        for end_tuple in positions:
            line, column = end_tuple
            end = Position()
            end.line = line
            end.column = column

            with pytest.raises(IndexError):
                Excerpt(buffer, start, end)
