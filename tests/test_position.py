from perivale import Position


def test_position():

    position = Position()
    assert position.__str__() == "[1:1]"
