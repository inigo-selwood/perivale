from .excerpt import Excerpt


class ParseError:

    def __init__(self):
        self.excerpts = []
    
    def __str__(self):
        return "\n".join([excerpt.__str__() for excerpt in self.excerpts])
    
    def add_excerpt(self, excerpt: Excerpt):
        self.excerpts.append(excerpt)