# Perivale

**Perivale:** The name of a stop on the London Underground, which alliterates with "parse buffer"

## Motivation

Most parsers implement a buffer object with methods for matching common text patterns. Some of those methods include:

- Peeking the next character in the stream
- Checking for a substring or RegEx match
- Parsing common tokens (identifiers, numbers, etc.)
- Skipping whitespace characters
- Backtracking to a certain position

In addition, a custom exception class `ParseError` is provided for informative error messages with references to lines or strings in the stream.

## Usage

### Finished

Checks whether the end of the stream has been reached

```python
>>> buffer = Buffer("")
>>> buffer.finished()
True
```

### Get Position

Get method for buffer's current position. 

```python
>>> buffer = Buffer("lorem ipsum")
>>> f"{buffer.copy_position()}"
'[1:1]'
>>>
>>> buffer.increment(steps=5)
>>> f"{buffer.copy_position()}"
'[1:6]'
>>>
>>> buffer.skip_line()
>>> f"{buffer.copy_position()}"
'[1:-1]'
```

**Note:** 

- Direct access to buffer's `position` attribute can result in undefined behaviour
- Column and line values start at 1. 
- Newlines are considered the last character of their line, and their index is represented as `[n:-1]`
- End-of-file is represented as `[-1:-1]`

### Set Position

Sets the buffer's position, checking for errors 

```python
>>> buffer = Buffer("lorem ipsum")
>>> buffer.set_position(buffer.position)
>>>
>>> buffer.set_position(Position(1, 1, 1))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File ".../perivale/buffer.py", in set_position
    raise IndexError(f"invalid position: {position}")
IndexError: invalid position: [1:1]
```

### Read

Reads the next character in the buffer. You can choose to skip that character after reading it

```python
>>> buffer = Buffer("lorem ipsum")
>>> buffer.read()
'l'
>>> buffer.read(consume=True)
'l'
>>> buffer.read()
'o'
```

### Match

Checks for an exact substring match. You can choose to skip the substring if it matches

```python
>>> buffer = Buffer("lorem ipsum")
>>> buffer.match("lorem ipsum")
True
>>>
>>> buffer.match("dolor sit amet")
False
>>>
>>> buffer.match("lorem ipsum", consume=True)
True
>>> buffer.finished()
True
```

### Skip Line

Skips an entire line of text

```python
>>> buffer = Buffer("lorem ipsum\ndolor sit amet")
>>> f"{buffer.position}"
'[1:1]'
>>>
>>> buffer.skip_line()
>>> f"{buffer.position}"
'[2:1]'
```

### Skip Whitespace

Skips whitespace characters (spaces, tabs, and optionally newlines)

```python
>>> buffer = Buffer(" \t\v\r")
>>> buffer.skip_space()
>>> buffer.finished()
True
>>>
>>> buffer = Buffer(" \t\v\r\n")
>>> buffer.skip_space(include_newlines=True)
>>> buffer.finished()
True
```

### Get Line

Gets the text on a given line

```python
>>> buffer = Buffer("lorem ipsum\ndolor sit amet")
>>> buffer.line_text()
'lorem ipsum'
>>> buffer.line_text(1)
'lorem ipsum'
>>> buffer.line_text(2)
'dolor sit amet'
```

**Note:** Line numbers are indexed from 1

### Get indentation

Gets the indentation level of a given line

```python
>>> text = """lorem ipsum
    dolor sit amet""""
>>> buffer = Buffer(text)
>>> buffer.line_indentation()
0
>>> buffer.line_indentation(1)
4
```

**Note:** Spaces are counted individually, tabs count as four spaces