from perivale import Buffer


def in_range(character: str, lower: str, upper: str) -> bool:
    character = ord(character)
    lower = ord(lower)
    upper = ord(upper)

    if lower >= upper:
        raise ValueError(f"illogical range ({lower} >= {upper}")

    return character >= lower and character <= upper