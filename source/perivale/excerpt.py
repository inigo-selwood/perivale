from __future__ import annotations

from .position import Position


class Excerpt:

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
