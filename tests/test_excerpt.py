from perivale import Buffer, Excerpt, Position


def test_excerpt():

    text = """lorem ipsum
dolor sit amet"""
    buffer = Buffer(text)

    # Simple
    position = Position(0, 1, 1)
    excerpt = Excerpt(buffer, position)
    assert f"{excerpt}" == """[1:1]
lorem ipsum
^"""

    # At position
    position = Position(6, 1, 7)
    excerpt = Excerpt(buffer, position)
    assert f"{excerpt}" == """[1:7]
lorem ipsum
      ^"""
        
    # At end of line
    position = Position(11, 1, -1)
    excerpt = Excerpt(buffer, position)
    assert f"{excerpt}" == """[1:-1]
lorem ipsum
           ^"""
    
    # At end of file
    position = Position(len(text), -1, -1)
    excerpt = Excerpt(buffer, position)
    assert f"{excerpt}" == """[-1:-1]
dolor sit amet
              ^"""