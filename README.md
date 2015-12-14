# Arcyóu
Arcyóu is a LISP-like functional programming language suitable for code golf. It has a large library of potentially useful functions, all one or two characters in length.

# Examples

Here are some real [PPCG](http://codegolf.stackexchange.com) puzzles which Arcyóu can solve in a small amount of bytes:

["Hello, World!"](http://codegolf.stackexchange.com/questions/55422/):

    "Hello, World!"  ; 15 bytes

[Golf you a quine for great good!](http://codegolf.stackexchange.com/questions/69/):

    Q  ; 1 byte?!

[Implement a Truth-Machine](http://codegolf.stackexchange.com/questions/62732/):

    (?(#(l))(@ 1(p 1))0  ; 19 bytes

[Is this number a prime?](http://codegolf.stackexchange.com/questions/57617/):

    (p?(#(l  ; 7 bytes

[Output the current time](http://codegolf.stackexchange.com/questions/65020/):

    (@ t(pn(zz 1)(p(st %H:%M:%S  ; 27 bytes

# Motivation

I would be lying if I didn't admit that I picked the Lisp syntax partially because of how easy it was to parse. But the idea behind Arcyóu is for it to be the Mathematica of golfing languages and have a builtin for everything, a feature which should easily offset the byte cost of parentheses.

# Executing code

To run an Arcyóu program you find on the Web somewhere, save it to a file, then run `arc.py` in a Python 3.x interpreter with the file's name as a command-line argument. Example in a bash shell:

    $ python3 arc.py myprogram.arc

You can also run the interpreter without any arguments to start an interactive read-eval-print loop, or REPL, session. Here's an example session:

    $ python3 arc.py
    Arcyóu version v0.1a. Copyright (C) 2015 Benjamin Kulas.
    This program comes with ABSOLUTELY NO WARRANTY; for details see the source code or the GNU General Public License version      3.

    Type (bye) or press Ctrl-C to exit.
    
    (油:0)>(+ 1 2)
    3
    (油:1)>(p? 997)
    False
    (油:2)>(r * (' 1 2 3 4
    24
    (油:3)>(bye)
    Bye.
    $

# Documentation

The documentation is a work in progress, but what there is of it can be found on the wiki for [Arcyóu's GitHub repository](https://github.com/nazek42/arcyou).

# Licensing

Arcyóu is licensed under the GNU GPL version 3. The full text of the license can be found on the official GNU webpage at http://www.gnu.org/licenses/gpl-3.0.txt.
