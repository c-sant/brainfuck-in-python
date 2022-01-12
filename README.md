# Brainfuck Interpreter in Python

> An implementation of an interpreter for the Brainfuck esoteric language in Python.

## :brain: The Brainfuck Language

Created in 1993 by Urban Müller, Brainfuck is an esoteric programming language, which means it is not supposed to be used for production.
It is widely known for its minimalist syntax, having only eight commands in total. 

It's name comes from the fact that it is very difficult to write meaningful and useful logic using the language, as the syntax can get
very confusing and unreadable.

## :grey_question: How to use

In Brainfuck, we have an array will unsigned bytes, which means it has an indefinite amount of cells containing numbers from 0 to 255.
The "traditional dialect" had 30000 cells, but newer interpreters sometimes include larger buffers with different types of data to store
more than 255 or negative values.

To traverse through memory, we use a **data pointer**, which points to one cell at a time. Operations are made based on the value at the pointer.
The eight commands we have to manipulate values are:

- ``>``: moves the pointer to the right;
- ``<``: moves the pointer to the left;
- ``+``: increments value currently at the pointer by 1;
- ``-``: decrements value currently at the pointer by 1;
- ``.``: prints the value at the current pointer;
- ``,``: replaces the value at the pointer by a user input;
- ``[``: if value at pointer is 0, goes to the next ``]`` in the code;
- ``]``: if value at pointer is not 0, goes back to the first ``[`` it finds in the code.

The latter two are used to create loops. When we hit a ``[``, we either execute everything until the next ``]`` or we just skip it all. Once
we get to the ``]``, if the value at the pointer is 0, we just keep going and executing the rest of the code; otherwise, we go all the way back
to the matching ``[`` and start executing everything again.

It is usual to translate the value to its ASCII table equivalent when the ``.`` command is executed. Therefore, a cell containing a value of ``65``
comes out as an ``a``. That's how you create your first "Hello World!" application, for example.

There are no if statements or comparison operators, people usually find work-arounds when those are needed using the loops.

### The Python interpreter

There are two classes in the Python package: ``Brainfuck`` (the interpreter) and ``BrainfuckException`` (in case something goes wrong). 

The Brainfuck interpreter accepts two arguments: 

- ``safe`` (bool): safe-mode. When turned off, Brainfuck errors raise the ``BrainfuckException`` in Python, which behaves as a regular exception in
application. When turned on, Brainfuck errors are only printed. Default value is **True** (turned on);
- ``memory_size``: (int): the size of the buffer array. Default value is **30000**.

When instantiated, the interpreter has three methods:
- ``run_file``: reads and interprets a .bf/.b file;
- ``prompt``: opens the Brainfuck interpreter in the terminal;
- ``run``: receives and interprets a string with Brainfuck code.

The memory array is stored in the ``data`` property, which can be accessed anytime by using ``instance.data``, where instance is a Brainfuck interpreter
instance.

## Example:

The following program is used to print "Hello, World!" to the screen:

```
>++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<+
+.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-
]<+.
```

## 💻 Requirements

The following setup was used to make the source code on this repository:

* Windows 10
* Python 3.10
* Numpy
