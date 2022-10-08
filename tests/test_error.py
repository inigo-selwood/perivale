from perivale import Buffer, ParseError


def test_error():
    text = """lorem ipsum
dolor sit amet
"""
    buffer = Buffer(text, source="/test.txt")

    error = ParseError()
    error.add_excerpt("error", buffer.excerpt())
    assert f"{error}".replace("\t", "    ") == """error
    [1:1] (/test.txt)
    lorem ipsum
    ^"""