import pytest

from perivale import Buffer


def test_position_valid():

    text = """lorem ipsum
dolor sit amet,
consectetur adipiscing"""
    buffer = Buffer(text)

    while not buffer.finished():
        position = buffer.copy_position()
        assert buffer.position_valid(position)
        buffer.increment()


def test_increment():

    # Simple (1 step)
    buffer = Buffer(".")
    buffer.increment()
    assert buffer.finished()

    # Multiple steps
    buffer = Buffer("...")
    buffer.increment(steps=3)
    assert buffer.finished()


def test_finished():

    # Empty
    assert Buffer("").finished()

    # Non-empty
    assert not Buffer(" ").finished()


def test_read():

    # Read
    buffer = Buffer(".")
    assert buffer.read() == "."
    assert not buffer.finished()

    # Read, consuming
    assert buffer.read(consume=True) == "."
    assert buffer.finished()

    # Read, buffer finished
    assert buffer.read() == ""


def test_match():

    # Match
    buffer = Buffer("lorem ipsum")
    assert buffer.match("lorem ipsum")
    
    # No match
    assert not buffer.match("dolor sit amet")

    # Match, consuming
    assert buffer.match("lorem ipsum", consume=True)
    assert buffer.finished()


def test_skip_line():
    buffer = Buffer("1\n2\n")
    assert buffer.read("1")

    buffer.skip_line()
    assert buffer.read("2")

    buffer.skip_line()
    assert buffer.finished()


def test_skip_space():

    # Whitespace
    buffer = Buffer(" \t\v\r")
    buffer.skip_space()
    assert buffer.finished()

    # Whitespace and newlines
    buffer = Buffer(" \t\v\r\n")
    buffer.skip_space(include_newlines=True)
    assert buffer.finished()


def test_line_text():

    # Current line
    buffer = Buffer("lorem ipsum\ndolor sit amet")
    assert buffer.line_text() == "lorem ipsum"

    # Arbitrary lines
    assert buffer.line_text(line_number=1) == "lorem ipsum"
    assert buffer.line_text(line_number=2) == "dolor sit amet"
    assert buffer.line_text(line_number=3) == ""

    # Invalid line number
    with pytest.raises(Exception):
        assert buffer.line_text(line_number=4)


def test_line_indentation():

    # Current line
    buffer = Buffer("  \n\t\n")
    assert buffer.line_indentation() == 2

    # Arbitrary line
    assert buffer.line_indentation(line_number=1) == 2
    assert buffer.line_indentation(line_number=2) == 4
    assert buffer.line_indentation(line_number=3) == 0

    # Invalid line number
    with pytest.raises(Exception):
        assert buffer.line_indentation(line_number=4)