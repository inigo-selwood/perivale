from perivale import Buffer


def _is_identifier(character: str, first_letter: bool) -> bool:
    ascii = ord(character)
    return (character == "_"
            or (ascii >= ord("a") and ascii <= ord("z"))
            or (ascii >= ord("A") and ascii <= ord("Z"))
            or (not first_letter and ascii >= ord("0") and ascii <= ord("9")))


def identifier_present(buffer: Buffer) -> bool:
    """ Checks whether an identifier is present
    
    An identifier is a string consisting of underscores, lower or uppercase 
    letters, and (non-leading) digits
    
    Arguments
    ---------
    buffer: Buffer
        the buffer to check in
    
    Returns
    -------
    present: bool
        if an identifier was found
    """

    return not buffer.finished() and _is_identifier(buffer.read(), True)


def parse_identifier(buffer: Buffer, consume: bool = False) -> str:
    """ Parses an identifier
    
    An identifier is a string consisting of underscores, lower or uppercase 
    letters, and (non-leading) digits
    
    Arguments
    ---------
    buffer: Buffer
        the buffer to parse from
    consume: bool
        if True, consumes the identifier
    
    Returns
    -------
    identifier: str
        the value of the identifier found
    
    Raises
    ------
    no_identifier: Exception
        if no identifier was found
    """

    text = ""
    position = buffer.copy_position()
    first_letter = True
    while not buffer.finished():

        character = buffer.read()
        if not _is_identifier(character, first_letter):
            break
        text += character
        buffer.increment()
        first_letter = False

    if not text:
        raise Exception("no identifier found")
    
    if not consume:
        buffer.position = position
    
    return text