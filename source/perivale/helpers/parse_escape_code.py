from perivale import Buffer, ParseError


def parse_escape_code(buffer: Buffer, 
        escape_codes: dict, 
        errors: list = [],
        consume: bool = False) -> str | None:
    
    # Sort the codes so none get dropped
    sorted_codes = []
    for symbol, code in escape_codes.items():

        if not symbol:
            raise ValueError("empty symbol")
        elif symbol == "\\" or symbol[0] != "\\":

            # Add the backslash prefix, check that wasn't already in the dict
            symbol = f"\\{symbol}"
            if symbol in escape_codes:
                raise ValueError(f"duplicate escape code: '{symbol}'")

        # Insert with precedence
        for index in range(len(sorted_codes)):
            predecessor = sorted_codes[index][0]
            if symbol[:len(predecessor)] == predecessor:
                sorted_codes.insert(index, (symbol, code))
                break
        else:
            sorted_codes.append((symbol, code))
    
    # Check for a match with each pair
    for pair in sorted_codes:
        symbol, code = pair
        if buffer.match(symbol, consume=consume):
            return code
    
    # Check a code was, indeed, present
    if not buffer.match("\\"):
        raise Exception("expected an escape code")
    
    code_position = buffer.copy_position()
    buffer.increment()

    # Report unfinished/invalid code
    if buffer.finished():
        error = ParseError()
        error.add_excerpt("incomplete escape code", 
                buffer.excerpt(code_position))
        errors.append(error)
        return None
    else:
        error = ParseError()
        error.add_excerpt("invalid escape code", 
                buffer.excerpt(code_position))
        errors.append(error)
        return None