from __future__ import annotations

from .excerpt import Excerpt
from .position import Position


class ParseError:

    def __init__(self, buffer):
        self.buffer = buffer
        self.excerpts = []
    
    def __str__(self) -> str:
        return "\n".join([excerpt.__str__() for excerpt in self.excerpts])
    
    def add_excerpt(self, message: str, 
            start: Position = None, 
            end: Position = None):
        
        excerpt = Excerpt(self.buffer, start, end, message)
        self.excerpts.append(excerpt)