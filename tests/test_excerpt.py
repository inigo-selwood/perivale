import pytest

from perivale import Buffer, PointExcerpt, RangeExcerpt, Position


def test_point_excerpt():

    text = """lorem ipsum
dolor sit amet,
consectetur adipiscing"""
    buffer = Buffer(text)

    # Simple
    position = Position(0, 1, 1)
    excerpt = PointExcerpt(buffer, position)
    assert excerpt.__str__() == """[1:1]
lorem ipsum
^"""

    # At position
    position = Position(6, 1, 7)
    excerpt = PointExcerpt(buffer, position)
    assert excerpt.__str__() == """[1:7]
lorem ipsum
      ^"""
        
    # At end of line
    position = Position(11, 1, -1)
    excerpt = PointExcerpt(buffer, position)
    assert excerpt.__str__() == """[1:-1]
lorem ipsum
           ^"""
    
    # At end of file
    position = Position(len(text), -1, -1)
    excerpt = PointExcerpt(buffer, position)
    assert excerpt.__str__() == """[-1:-1]
consectetur adipiscing
                      ^"""
    

def test_range_excerpt():

    text = """lorem ipsum
dolor sit amet,
consectetur adipiscing"""
    buffer = Buffer(text)

    start = Position(0, 1, 1)

    # Simple
    end = Position(5, 1, 6)
    excerpt = RangeExcerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:1 - 6]
lorem ipsum
^^^^^"""

    # Over two lines
    end = Position(17, 2, 5)
    end.line = 2
    end.column = 6
    excerpt = RangeExcerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:1 - 2:6]
lorem ipsum
^^^^^^^^^^^
dolor sit amet,
^^^^^"""

    # Over more than two lines
    end = Position(39, 3, 12)
    excerpt = RangeExcerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:1 - 3:12]
lorem ipsum
^^^^^^^^^^^
...
consectetur adipiscing
^^^^^^^^^^^"""

    # Starting at newline (caret should be elided)
    start = Position(11, 1, -1)
    end = Position(17, 2, 6)

    excerpt = RangeExcerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:-1 - 2:6]
lorem ipsum
dolor sit amet,
^^^^^"""

    # Ending at newline
    start = Position(0, 1, 1)
    end = Position(11, 1, -1)
    excerpt = RangeExcerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:1 - -1]
lorem ipsum
^^^^^^^^^^^"""

    # Ending at start-of-line
    end = Position(12, 2, 1)
    excerpt = RangeExcerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:1 - 2:1]
lorem ipsum
^^^^^^^^^^^
dolor sit amet,"""

    # Ending at newline, starting at start-of-line
    start = Position(11, 1, -1)
    excerpt = RangeExcerpt(buffer, start, end)
    assert excerpt.__str__() == """[1:-1 - 2:1]
lorem ipsum
dolor sit amet,"""

    # Ending at end-of-file
    start = Position(28, 3, 1)
    end = Position(len(text), -1, -1)
    excerpt = RangeExcerpt(buffer, start, end)
    assert excerpt.__str__() == """[3:1 - -1:-1]
consectetur adipiscing
^^^^^^^^^^^^^^^^^^^^^^"""    
