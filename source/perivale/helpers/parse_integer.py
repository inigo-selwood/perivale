from perivale import Buffer


def _is_decimal(character: str) -> bool:
        character = ord(character)
        return character >= ord("0") and character <= ord("9")

  
def _is_hexadecimal(character: str) -> bool:
    character = ord(character)
    return ((character >= ord("0") and character <= ord("9"))
            or (character >= ord("a") and character <= ord("f"))
            or (character >= ord("A") and character <= ord("F")))


def _is_octal(character: str) -> bool:
    character = ord(character)
    return character >= ord("0") and character <= ord("7")


def _is_binary(character: str) -> bool:
    return character == "0" or character == "1"


def integer_present(buffer: Buffer, base: int = 10) -> bool:
    """ Checks whether an integer value of a given base is present

    Bases supported:

        10: decimal
        16: hexadecimal
        8: octal
        2: binary
    
    Arguments
    ---------
    buffer: Buffer
        buffer to check in
    base: int
        the base of the integer (defaults to 10, decimal)
    
    Returns
    -------
    present: bool
        True if an integer of that base is present
    
    Raises
    ------
    bad_base: ValueError
        if the base specified isn't supported
    """

    base_validators = {
        10: _is_decimal,
        16: _is_hexadecimal,
        2: _is_binary,
        8: _is_octal,
    }

    if base not in base_validators:
        raise ValueError(f"unsupported base: {base}")
    validator = base_validators[base]

    return not buffer.finished() and validator(buffer.read())


def parse_integer(buffer: Buffer, 
        base: int = 10, 
        consume: bool = False) -> int:
    
    """ Parses an integer value of a given base

    Bases supported:

        10: decimal
        16: hexadecimal
        8: octal
        2: binary
    
    Arguments
    ---------
    buffer: Buffer
        buffer to check in
    base: int
        the base of the integer (defaults to 10, decimal)
    consume: bool
        if True, consumes the integer
    
    Returns
    -------
    value: int
        the parsed value, cast to an integer
    
    Raises
    ------
    no_integer: Exception
        if no integer was found (check first)
    bad_base: ValueError
        if the base specified isn't supported
    """

    base_validators = {
        10: _is_decimal,
        16: _is_hexadecimal,
        2: _is_binary,
        8: _is_octal,
    }

    if base not in base_validators:
        raise ValueError(f"unsupported base: {base}")
    validator = base_validators[base]

    text = ""
    position = buffer.copy_position()
    while not buffer.finished():

        character = buffer.read()
        if not validator(character):
            break
        text += character
        buffer.increment()

    if not text:
        raise Exception("no integer found")
    
    if not consume:
        buffer.position = position
    
    return int(text, base)