from copy import copy

from .position import Position
from .excerpt import PointExcerpt, RangeExcerpt


class Buffer:

    def __init__(self, text: str, source: str = ""):
        self.text = text
        self.length = len(text)
        self.source = source

        self.line_indices = []
        self.line_indentations = []
        self.line_count = 0
        
        index = 0
        while index < self.length:
            self.line_indices.append(index)
        
            # Evaluate indentation
            indentation = 0
            while True:
                if index == self.length:
                    break
            
                if text[index] == "\t":
                    indentation = ((indentation + 4) & ~0x03)
                elif text[index] == " ":
                    indentation += 1
                else:
                    break
            
                index += 1
            self.line_indentations.append(indentation)

            # Move to next newline
            while index < self.length and text[index] != '\n':
                index += 1
            index += 1
        
        self.line_count = len(self.line_indices)
        
        self.position = Position()
        if not text:
            self.position.line = -1
            self.position.column = -1
        elif text[0] == "\n":
            self.position.column = -1
    
    def position_valid(self, position: Position):
        """ Checks whether a given position is valid for this buffer
        
        Arguments
        ---------
        position: Position
            the position to check
        
        Returns
        -------
        valid: bool
            true if the position is valid
        """

        index, line, column = position.index, position.line, position.column

        if index == self.length and line == -1 and column == -1:
            return True

        if index > self.length or line > self.line_count:
            return False
        
        start = self.line_indices[line - 1]
        if line == self.line_count and column == -1:
            return index == self.length - 1
        
        if column == -1:
            if line == self.line_count:
                return index == self.length
            
            next_index = self.line_indices[line]
            return index == next_index - 1
        
        return index == start + column - 1        

    def increment(self, steps: int = 1):
        """ Increments the buffer's position
        
        Arguments
        ---------
        steps: int
            the number of steps to increment
        """

        for _ in range(steps):

            # Stop when the end of the buffer has been reached
            if self.position.index >= self.length:
                return

            # If the current character is a newline, increment the line number
            # and reset the column
            character = self.text[self.position.index]
            if character == "\n":
                self.position.line += 1
                self.position.column = 1

            # Handle tabs by rounding up to the next multiple of 4 (+1)
            elif character == "\t":
                column = int(((self.position.column + 3) / 4) * 4 + 1)
                self.position.column = column

            # Failing the above, and if the character wasn't format-related,
            # increment the column
            else:

                value = ord(character)
                lower, upper = [ord(letter) for letter in [" ", "~"]]
                if value >= lower and value <= upper:
                    self.position.column += 1

            self.position.index += 1

            if self.position.index == self.length:
                self.position.column = -1
                self.position.line = -1
            elif self.text[self.position.index] == "\n":
                self.position.column = -1
    
    def finished(self) -> bool:
        """ Checks if the buffer is finished
        
        Returns
        -------
        finished: bool
            if the buffer is finished
        """
        
        return self.position.index == self.length
    
    def copy_position(self) -> Position:
        """ Copies the buffer's position
        
        Note: this method _must_ be used rather than using the position member 
        directly
        
        Returns
        -------
        position: Position
            the copied position
        """

        return copy(self.position)
    
    def set_position(self, position: Position):
        """ Sets the buffer's position, checking its validity
        
        Arguments
        ---------
        position: Position
            the position to set
        
        Raises
        ------
        error: IndexError
            if the position is invalid
        """

        if not self.position_valid(position):
            raise IndexError(f"invalid position: {position}")
        self.position = copy(position)
    
    def read(self, consume: bool = False) -> str:
        """ Reads the next character from the buffer
        
        Arguments
        ---------
        consume: bool
            if True, increments past the read character
            
        Returns
        -------
        character: str
            the character read, or "" if the buffer is finished
        """

        if self.finished():
            return ""
        
        result = self.text[self.position.index]
        if consume:
            self.increment()
        return result
    
    def match(self, text: str, consume: bool = False) -> bool:
        """ Checks whether a substring matches
        
        Arguments
        ---------
        text: str
            the substring to match
        consume: bool
            if true (and the substring matches), increments past it
        
        Returns
        -------
        match: bool
            true if the substring matched
        """

        if self.finished():
            return False
        
        # Check match feasible
        length = len(text)
        if self.position.index + length > self.length:
            return False
        
        # Extract substring
        end = self.position.index + length
        substring = self.text[self.position.index:end]

        # Check for match
        result = text == substring
        if result and consume:
            self.increment(steps=length)
        
        return result

    def skip_line(self):
        """ Skips the current line """

        if self.position.line >= self.line_count:
            self.position.index = self.length
            self.position.column = -1
        else:
            index = self.line_indices[self.position.line]
            self.position.index = index
            self.position.line += 1
            self.position.column = 1

    def skip_space(self, include_newlines: bool = False):
        """ Skips whitespace characters
        
        Arguments
        ---------
        include_newlines: bool
            if true, skips newlines as well
        """
        while not self.finished():
            character = self.text[self.position.index]

            if ((character not in " \t\v\r") and 
                    not (character == "\n" and include_newlines)):
                break

            self.increment()

    def line_text(self, line_number: int = 0) -> str:
        """ Gets the text of a given line
        
        Arguments
        ---------
        line_number: int
            the number of the line of text to fetch; Note: not zero-indexed! By
            default, gets the current line's text
        
        Returns
        -------
        text: str
            the given line's text
        """

        # Set line number to current if zero, or last line if -1
        if line_number == 0:
            line_number = self.position.line
        elif line_number == -1:
            line_number = self.line_count

        # Assert line number in range
        if line_number < 1 or line_number > self.line_count:
            return ""

        # Evaluate start index
        start_index = 0
        if line_number > 1:
            start_index = self.line_indices[line_number - 1]

        # Evaluate end index
        end_index = self.length
        if line_number < self.line_count:
            end_index = self.line_indices[line_number] - 1
        elif self.length and self.text[self.length - 1] == "\n":
            end_index = self.length - 1

        return self.text[start_index:end_index]

    def line_indentation(self, line_number: int = 0) -> int:
        """ Gets the indentation of a given line
        
        Arguments
        ---------
        line_number: int
            the number of the line whose indentation to fetch; Note: not 
            zero-indexed! By default, gets the current line's indentation
        
        Returns
        -------
        indentation: int
            the given line's indentation
        """

        # Set line number to current if zero, or last line if -1
        if line_number == 0:
            line_number = self.position.line
        elif line_number == -1:
            line_number = self.line_count

        # Check line is in bounds
        if line_number < 1 or line_number > self.line_count:
            return 0

        return self.line_indentations[line_number - 1]
    
    def point_excerpt(self, position: Position = None) -> PointExcerpt:
        """ Creates a point excerpt

        If no position is given, the current buffer position is inferred
        
        Arguments
        ---------
        position: Position
            the position of the excerpt
        
        Returns
        -------
        excerpt: PointExcerpt
            the excerpt created
        
        Raises
        ------
        position_invalid: ValueError
            if the position given is invalid
        """

        if not position:
            position = self.copy_position()
        return PointExcerpt(self, position)
    
    def range_excerpt(self, start: Position, end: Position = None):
        """ Creates a range excerpt

        If no end position is given, the current buffer position is inferred
        
        Arguments
        ---------
        start: Position
            position of the excerpt start
        end: Position
            position of the excerpt end
        
        Returns
        -------
        excerpt: RangeExcerpt
            the excerpt created
        
        Raises
        ------
        position_invalid: ValueError
            if one of the positions given is invalid
        position_illogical: IndexError
            if the range given (or inferred) doesn't make sense, ie: the start
            position succeeds the end
        """
        
        if not end:
            end = self.copy_position()
        return RangeExcerpt(self, start, end)