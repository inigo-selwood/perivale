from __future__ import annotations


class Position:

    class Delta:

        def __init__(self, start: Position, end: Position):
            self.start = start
            self.end = end

            if ((start.line == end.line 
                        and end.column != -1 
                        and start.column >= end.column)
                    or start.line > end.line):
                raise IndexError("start postion comes after end")

        def __str__(self) -> str:
            start, end = (self.start, self.end)
            if start.line == end.line:
                return f"[{start.line}:{start.column} - {end.column}]"
            
            return f"[{start.line}:{start.column} - {end.line}:{end.column}]"

    def __init__(self, index: int = 0, line: int = 1, column: int = 1):
        self.index = index
        self.line = line
        self.column = column
    
    def __str__(self) -> str:
        return f"[{self.line}:{self.column}]"