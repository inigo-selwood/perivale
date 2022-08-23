# Perivale

**Perivale:** The name of a stop on the London Underground, which alliterates with "parse buffer"

## Motivation

Most parsers implement a buffer object with methods for matching common text patterns. Some of those methods include:

- Peeking the next character in the stream
- Checking for a substring or RegEx match
- Parsing common tokens (identifiers, numbers, etc.)
- Skipping whitespace characters
- Backtracking to a certain position

In addition, a custom exception class `ParseException` is provided for informative error messages with references to lines or strings in the stream.

## Usage

### Finished

Checks whether the end of the stream has been reached

```python
>>> buffer = Buffer("")
>>> buffer.finished()
True
```

### Copy Position

Gets a deep copy of the buffer's current position. Can be used to store the position of certain tokens, or backtrack the buffer on error

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
'[1:-1]'
```

**Note:** 

- Column and line values start at 1. 
- Newlines are considered the last character of their line, and their index is represented as `[n:-1]`
- End-of-file is represented as `[-1:-1]`

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