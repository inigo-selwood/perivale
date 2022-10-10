from perivale import Buffer


def parse_identifier(buffer: Buffer, consume: bool = False) -> str:

    text = ""
    position = buffer.copy_position()
    while not buffer.finished():

        character = buffer.read()
        ascii = ord(character)
        if (character != "_"
                and (ascii < ord("a") or ascii > ord("z"))
                and (ascii < ord("A") or ascii > ord("Z"))
                and (not text or ascii < ord("0") or ascii > ord("9"))):
            break
        text += character
        buffer.increment()

    if not text:
        raise Exception("no identifier found")
    
    if not consume:
        buffer.position = position
    
    return text