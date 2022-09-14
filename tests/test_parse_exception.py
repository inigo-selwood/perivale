from perivale import Buffer, ParseException, Set


def test_parse_exception():

    buffer = Buffer("lorem ipsum\ndolor sit amet")
    exception = ParseException("message", buffer)
    assert f"{exception}" == """[1:1] (message)
    lorem ipsum
    ^"""

    buffer.skip_line()
    exception = ParseException("message", buffer)
    assert f"{exception}" == """[2:1] (message)
    dolor sit amet
    ^"""

    buffer.increment(steps=6)
    exception = ParseException("message", buffer)
    assert f"{exception}" == """[2:7] (message)
    dolor sit amet
          ^"""

    buffer.skip_line()
    exception = ParseException("message", buffer)
    assert f"{exception}" == """[2:-1] (message)
    dolor sit amet
                  ^"""

    buffer = Buffer("\n")
    buffer.skip_space(include_newlines=True)
    exception = ParseException("message", buffer)
    assert f"{exception}" == """[1:-1] (message)
    
    ^"""

