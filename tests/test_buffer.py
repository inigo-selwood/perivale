from perivale import Buffer, Set


def test_increment():

    buffer = Buffer(".")
    buffer.increment()
    assert buffer.finished()

    buffer = Buffer("...")
    buffer.increment(steps=3)
    assert buffer.finished()


def test_finished():
    assert Buffer("").finished()
    assert not Buffer(" ").finished()


def test_read():
    buffer = Buffer(".")
    assert buffer.read() == "."

    assert buffer.read(consume=True) == "."
    assert buffer.finished()


def test_match():
    buffer = Buffer("lorem ipsum")
    assert buffer.match("lorem ipsum")
    
    assert not buffer.match("dolor sit amet")

    assert buffer.match("lorem ipsum", consume=True)
    assert buffer.finished()


def test_parse_set():
    buffer = Buffer("lowercase")
    assert buffer.parse_set(Set.LOWERCASE) == "lowercase"

    assert buffer.parse_set(Set.LOWERCASE, consume=True) == "lowercase"
    assert buffer.finished()


def test_parse_range():
    buffer = Buffer("lorem ipsum")
    assert buffer.parse_range((" ", "~")) == "lorem ipsum"

    assert buffer.parse_range((" ", "~"), consume=True) == "lorem ipsum"
    assert buffer.finished()


def test_parse_bounded_text():

    # Simple bounded text
    buffer = Buffer("'a string'")
    assert buffer.parse_bounded_text(("'", "'")) == "'a string'"
    
    # No start token match
    buffer = Buffer("a string'")
    assert buffer.parse_bounded_text(("'", "'")) == ""
    
    # No end token match
    buffer = Buffer("'a string")
    assert buffer.parse_bounded_text(("'", "'")) == ""
   
    # Bounded text with escaped end code
    buffer = Buffer("'\\''")
    assert buffer.parse_bounded_text(("'", "'"), escape_bounds=True) == "'''"

    # Escape codes
    escape_codes = {
        "\\v": "\v",
        "\\t": "\t",
        "\\r": "\r",
        "\\n": "\n",
    }
    buffer = Buffer("'\\v\\t\\r\\n'")
    result = buffer.parse_bounded_text(("'", "'"), escape_codes=escape_codes)
    assert result == "'\v\t\r\n'"

    # Nested escaped end codes
    buffer = Buffer("<<\\>>")
    result = buffer.parse_bounded_text(("<", ">"), escape_bounds=True)
    assert result == "<<>>"

    # Disallowed newline
    buffer = Buffer("'\n'")
    assert buffer.parse_bounded_text(("'", "'")) == ""

    # Permitted newline
    result = buffer.parse_bounded_text(("'", "'"), permit_newlines=True)
    assert result == "'\n'"


def test_skip_line():

    buffer = Buffer("1\n2\n")
    assert buffer.read("1")

    buffer.skip_line()
    assert buffer.read("2")

    buffer.skip_line()
    assert buffer.finished()


def test_skip_space():

    buffer = Buffer(" \t\v\r")
    buffer.skip_space()
    assert buffer.finished()

    buffer = Buffer(" \t\v\r\n")
    buffer.skip_space(include_newlines=True)
    assert buffer.finished()


def test_line_text():

    buffer = Buffer("lorem ipsum\ndolor sit amet")
    assert buffer.line_text() == "lorem ipsum"
    assert buffer.line_text(line_number=1) == "lorem ipsum"
    assert buffer.line_text(line_number=2) == "dolor sit amet"
    assert buffer.line_text(line_number=3) == ""


def test_line_indentation():

    buffer = Buffer("  \n\t\n")
    assert buffer.line_indentation() == 2
    assert buffer.line_indentation(line_number=1) == 2
    assert buffer.line_indentation(line_number=2) == 4
    assert buffer.line_indentation(line_number=3) == 0