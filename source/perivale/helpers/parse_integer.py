from perivale import Buffer


def parse_integer(buffer: Buffer, base: int = 10, consume: bool = False):

    def is_decimal(character: str) -> bool:
        character = ord(character)
        return character >= ord("0") and character <= ord("9")
    
    def is_hexadecimal(character: str) -> bool:
        character = ord(character)
        return ((character >= ord("0") and character <= ord("9"))
                or (character >= ord("a") and character <= ord("f"))
                or (character >= ord("A") and character <= ord("F")))
    
    def is_octal(character: str) -> bool:
        character = ord(character)
        return character >= ord("0") and character <= ord("7")
    
    def is_binary(character: str) -> bool:
        return character == "0" or character == "1"
    
    base_validators = {
        10: is_decimal,
        16: is_hexadecimal,
        2: is_binary,
        8: is_octal,
    }

    if base not in base_validators:
        raise Exception(f"unsupported base: {base}")
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