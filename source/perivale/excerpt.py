from __future__ import annotations

from .position import Position


class Excerpt:

    def __init__(self, 
            buffer, 
            start: Position = None, 
            end: Position = None, 
            annotation: str = None):
        
        self.annotation = annotation

        # Check positions valid
        if start and not buffer.position_valid(start):
            raise IndexError("invalid start position")
        if end and not buffer.position_valid(end):
            raise IndexError("invalid end position")

        # Resolve position
        if not start:
            start = buffer.copy_position()
        elif end and end.index == start.index:
            end = None
        
        self.start = start
        self.end = end
        
        # Single line, single character
        self.text = ""
        if not end:
            line = buffer.line_text(start.line)
            index = start.column - 1 if start.column != -1 else len(line)
            caret = " " * index + "^"
            self.text = f"{line}\n    {caret}"

        # Single line, multiple characters
        elif start.line == end.line:
            line = buffer.line_text(start.line)
            start_index = start.column - 1
            end_column = end.column - 1 if end.column != -1 else len(line)
            caret = " " * start_index + "^" * (end_column - start_index)
            self.text = f"{line}\n    {caret}"

        # Multiple (adjacent) lines
        else:
            start_line = buffer.line_text(start.line)
            end_line = buffer.line_text(end.line)

            start_width = len(start_line)
            end_width = len(end_line)

            start_index = start.column - 1 
            if start.column == -1:
                start_index = start_width
            end_index = end.column - 1 if end.column != -1 else end_width
        
            start_caret = " " * start_index + "^" * (start_width - start_index)
            end_caret = "^" * end_index

            if start.column != -1:
                self.text = f"{start_line}\n    {start_caret}"
                if start.line + 1 != end.line:
                    self.text += "\n    ..."
                self.text += "\n    "
            
            self.text += f"{end_line}\n    {end_caret}"

    def __str__(self) -> str:
        position = self.start 
        if self.end:
            position = Position.Delta(self.start, self.end)

        result = f"{position}"
        if self.annotation:
            result += f"({self.annotation})"
        return result + f"\n    {self.text}"