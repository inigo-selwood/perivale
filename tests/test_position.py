from perivale import Position


def test_position():

    position = Position()
    assert position.__str__() == "[1:1]"


def test_delta():

    start = Position()
    end = Position()
    end.column = -1
    delta = Position.Delta(start, end)
    assert delta.__str__() == "[1:1 - -1]"

    end.line = 2
    end.column = 1
    delta = Position.Delta(start, end)
    assert delta.__str__() == "[1:1 - 2:1]"
