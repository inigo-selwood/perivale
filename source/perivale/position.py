from __future__ import annotations


class Position:

    def __init__(self, index: int = 0, line: int = 1, column: int = 1):
        self.index = index
        self.line = line
        self.column = column
    
    def __str__(self) -> str:
        return f"[{self.line}:{self.column}]"