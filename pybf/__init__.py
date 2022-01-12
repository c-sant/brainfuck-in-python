"""
Brainfuck is an esoteric programming language created in 1993 by Urban Müller. 
It's design was inspired by other esolangs, such as FALSE and P", and it is
said that Müller intended to create the smallest possible compiler.

Because of that, Brainfuck has a extreme minimalist syntax. The whole language
consists of eight simple commands, with every other character being ignored by
the compiler. Those commands manipulate a 30000-byte long array, and as
impressive as it is, Brainfuck is Turing complete, which means one technically
can build a C compiler using it.

The eight commands are:

>: increment the data pointer, pointing to the next cell in the array;
<: decrement the data pointer;
+: increment the byte at the data pointer;
-: decrement the byte at the data pointer;
.: output the byte at the data pointer;
,: accept one byte of input, storing it's value in the current byte at the data
pointer;
[: if current byte at the data pointer is zero, skips to the next ].
]: if the current byte is not zero, jumps back to the first [.

The two latter commands can be used to create loops. One [ matches exactly one ].
There can be no unmatching brackets.

Since Brainfuck doesn't recognize any character other than it's eight commands,
comments can be made anywhere as long as they don't include any of the special
characters.

Source: https://en.wikipedia.org/wiki/Brainfuck
"""

import numpy as np

class BrainfuckException(Exception):
    """
    Base Brainfuck exception.
    """

class Brainfuck:
    def __init__(self, memory_size: int = 30000, safe: bool = True):
        if memory_size < 0:
            raise ValueError('memory size cannot be negative')
            
        self._data = np.array([0] * memory_size)
        self._data = self._data.astype(np.ubyte)
        self.safe = safe
    
    @property
    def data(self):
        return self._data

    def run_file(self, file_path: str):
        if not file_path.endswith('.b') and not file_path.endswith('.bf'):
            self.__report_error('invalid file')
        
        with open(file_path, 'r') as f:
            code = f.read()

        self.run(code)


    def prompt(self):
        print("Brainfuck Interpreter\nInsert Brainfuck code below. Write /quit to quit.")

        while True:
            value = input('> ').lower().strip()
            if value == '/quit':
                return
            
            self.run(value)


    def run(self, code):
        had_error = self.__evaluate(code)
        
        if had_error: return

        self.__interpret(code)
        

    def __report_error(self, message: str, line: int = None, column: int = None):
        if line == None or column == None:
            print(f'[Brainfuck] exception: {message}')
        else:
            print(f'[Brainfuck] exception at line {line} char {column}: {message}')

        if not self.safe:
            raise BrainfuckException(message)


    def __evaluate(self, source: str):
        line = col = 0

        stk = []

        for c in source:
            match c:
                case '[':
                    stk.append('[')
                case ']':
                    if len(stk) == 0:
                        self.__report_error("unexpected token ']'", line, col)
                        return True
                    
                    stk.pop()
                case '\n':
                    line += 1
                    col = -1
                case _:
                    pass
            col += 1

        if len(stk) != 0:
            self.__report_error("unmatched brackets")
            return True

        return False


    def __interpret(self, source: str):
        line = col = ptr = current =  0

        while current < len(source):
            match source[current]:
                case '>':
                    if ptr == (len(self.data) - 1):
                        self.__report_error("pointer out of range", line, col)
                        return True

                    ptr += 1
                case '<':
                    if ptr == 0:
                        self.__report_error("pointer out of range", line, col)
                        return True

                    ptr -= 1
                case '+':
                    if self.data[ptr] == 255:
                        self.__report_error("cell overflow")
                        return True
                    
                    self.data[ptr] += 1

                case '-':
                    if self.data[ptr] == 0:
                        self.__report_error("cell underflow")
                        return True
                    
                    self.data[ptr] -= 1
                case '.':
                    print(chr(self.data[ptr]))
                case ',':
                    value = input()
                    if not value.isdigit():
                        self.__report_error("invalid input")
                    
                    self.data[ptr] = np.ubyte(value)
                case '[':
                    if self.data[ptr] == 0:
                        while source[current] != ']':
                            current += 1
                case ']':
                    if self.data[ptr] != 0:
                        while source[current] != '[':
                            current -= 1
                case '\n':
                    line += 1
                    col = -1
                case _:
                    pass
        
            col += 1
            current += 1

        return False
