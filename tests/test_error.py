from perivale import Buffer, ParseError


def test_error():

    text = """lorem ipsum
dolor sit amet,
consectetur adipiscing"""
    buffer = Buffer(text, source="/test.txt")

    error = ParseError()
    error.add_excerpt("error", buffer.point_excerpt())
    assert f"{error}".replace("\t", "    ") == """error
    [1:1] (/test.txt)
    lorem ipsum
    ^"""

    start = buffer.copy_position()
    buffer.skip_line()
    buffer.match("dolor", consume=True)

    error = ParseError()
    error.add_excerpt("error", buffer.range_excerpt(start))
    assert f"{error}".replace("\t", "    ") == """error
    [1:1 - 2:6] (/test.txt)
    lorem ipsum
    ^^^^^^^^^^^
    dolor sit amet,
    ^^^^^"""
