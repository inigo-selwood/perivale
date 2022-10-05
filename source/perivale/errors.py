from __future__ import annotations

from .excerpt import Excerpt


class ParseError:

    def __init__(self):
        self.excerpts = []
    
    def __str__(self) -> str:

        result = []
        for pair in self.excerpts:
            message, excerpt = pair
            annotated_excerpt = message

            lines = f"{excerpt}".split("\n")
            annotated_excerpt += "".join([f"\n\t{line}" for line in lines])
            result.append(annotated_excerpt)
        
        return "\n".join(result)
    
    def add_excerpt(self, message: str, excerpt: Excerpt):
        self.excerpts.append((message, excerpt))