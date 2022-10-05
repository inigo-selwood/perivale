from __future__ import annotations

from .position import Position


class Excerpt:

    def __init__(self):
        pass


class PointExcerpt(Excerpt):

    def __init__(self, buffer, position: Position):
        if not buffer.position_valid(position):
            raise ValueError("invalid position")

        self.source = buffer.source
        self.text = buffer.line_text(position.line)
        self.position = position
    
    def __str__(self):
        result = f"{self.position}"

        if self.source:
            result += f" ({self.source})"
        
        result += f"\n{self.text}"

        line_length = len(self.text)
        column = self.position.column
        caret_index = column - 1 if column != -1 else line_length
        caret = " " * caret_index + "^"
        result += f"\n{caret}"

        return result


class RangeExcerpt(Excerpt):

    def __init__(self, buffer, start: Position, end: Position):
        if not buffer.position_valid(start):
            raise ValueError("invalid start position")
        elif not buffer.position_valid(end):
            raise ValueError("invalid end position")
        elif start.index >= end.index:
            raise IndexError("illogical range start/end")
        
        self.source = buffer.source

        if start.line == end.line:
            self.lines = [buffer.line_text(start.line)]
        else:
            self.lines = [
                buffer.line_text(start.line),
                buffer.line_text(end.line),
            ]
        
        self.start = start
        self.end = end
    
    def __str__(self):
        result = ""

        start_line, start_column = self.start.line, self.start.column
        end_line, end_column = self.end.line, self.end.column

        if self.start.line == self.end.line:
            result = f"[{start_line}:{start_column} - {end_column}]"
        else:
            result = f"[{start_line}:{start_column} - {end_line}:{end_column}]"

        if self.source:
            result += f" ({self.source})"

        # Single line
        if start_line == end_line:
            line = self.lines[0]
            start_index = start_column - 1
            end_column = end_column - 1 if end_column != -1 else len(line)
            caret = " " * start_index + "^" * (end_column - start_index)
            result += f"\n{line}\n{caret}"

        # Multiple lines
        else:
            start_text, end_text = self.lines
            start_width = len(start_text)
            end_width = len(end_text)

            start_index = start_column - 1 
            if start_column == -1:
                start_index = start_width
            end_index = end_column - 1 if end_column != -1 else end_width

            result += f"\n{start_text}"
            if start_column != -1 or start_line + 1 != end_line:
                caret_width = start_width - start_index
                result += "\n" + " " * start_index + "^" * caret_width

            if start_line + 1 != end_line:
                result += "\n..."

            result += f"\n{end_text}"
            if end_column != 1:
                result += "\n" + "^" * end_index
        
        return result