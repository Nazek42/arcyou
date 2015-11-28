# Arcyou's function library.

# Copyright 2015 Benjamin Kulas
#
# This file is part of Arcyóu.
#
# Arcyóu is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Arcyóu is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Arcyóu.  If not, see <http://www.gnu.org/licenses/>.

from types import FunctionType
from error import *
from collections import Hashable
import sys
import functools
import time

class ArcFunction:
    """
A function in live code is represented by this.
    """
    def __init__(self, params, body):
        self.params = params[:]
        self.body = body[:]
    def __repr__(self):
        return "F(%s)" % ' '.join(self.params)
    def __call__(self, *args):
        global ArcNamespace
        #print("ArcFunction's args:", args)
        for param, arg in zip(self.params, args):
            ArcNamespace[param] = arg
        # Fixpoint
        ArcNamespace['$'] = ArcFunction(self.params, self.body)
        result = ArcEval(self.body)
        for param in self.params:
            if param in ArcNamespace:
                ArcNamespace.pop(param)
        if '$' in ArcNamespace:
            ArcNamespace.pop('$')
        return result

def ArcEval(cons):
    """
The core of Arcyou, a work of intricate recursion.
*This* is what executes code.
Arguments: cons <-- A single Arcyou cell
Returns: the result of evaluating that cell. The only thing that is guaranteed
is that you won't get another cell.
    """
    global ArcNamespace
#    print("cons:", cons)
    # Is it an atom?
    if is_num(cons):
        return cons
    if is_string_literal(cons):
        return cons[1:-1]
    if isinstance(cons, Hashable):
        if cons in ArcNamespace:
            return ArcNamespace[cons]
        else:
            return cons
    # Is it a special form?
#    print("Hello from special form handler")
    func = cons[0]
    # If
    if func == '?':
        cond = ArcEval(cons[1])
        return ArcIf(cond, *cons[2:4])
    # While
    if func == '@':
        return ArcWhile(*cons[1:3])
    # For
    if func == 'f':
        iterator = ArcEval(cons[2])
        return ArcFor(cons[1], iterator, cons[3])
    # Function
    if func == 'F':
        return ArcFunction(cons[1], cons[2])
    # Set
    if func == ':':
        value = ArcEval(cons[2])
        ArcNamespace[cons[1]] = value
        return value
    # Quote
    if func == '\'':
        return cons[1:]

    # Not an atom or a special form?
    # It must be a function call!
    # Resolve *everything*. This will get already-defined functions as well.
    #print("Hello from function handler")
    #print("func:", func)
    consr = [ArcEval(thing) for thing in cons]
    funcr = consr[0]
    #print("funcr:", repr(funcr))
    arguments = consr[1:]
    #print("arguments:", arguments)

    # Implicit indexing
    if isinstance(funcr, list):
        result = _index_slice(funcr, arguments)
    elif arguments != []:
        result = funcr(*arguments)
    else:
        result = funcr()
    #print("result:", result)
    return result

def is_num(thing):
    """Check if an object is a numeric type."""
    if isinstance(thing, (int, float)):
        return True
    else:
        return False

def is_string_literal(thing):
    """Check if a symbol is actually a string literal."""
    if isinstance(thing, str):
        if thing.startswith('"') and thing.endswith('"'):
            return True
        else:
            return False
    return False

def ArcIf(cond, iftrue, iffalse):
    """If-statement."""
    if cond:
        return ArcEval(iftrue)
    else:
        return ArcEval(iffalse)

def ArcFor(symbol, iterator, body):
    """For loop/listcomp."""
    global ArcNamespace
    result = []
    for item in iterator:
        ArcNamespace[symbol] = item
        result.append(ArcEval(body))
    if symbol in ArcNamespace:
        ArcNamespace.pop(symbol)
    return result

def ArcWhile(cond, body):
    """While loop/incredibly abstract comprehension."""
    result = []
    while ArcEval(cond):
        result.append(ArcEval(body))
    return result

def _add(*args):
    if len(args) == 1:
        return sum(args[0])
    else:
        return sum(args)

def _percent(x, y):
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return x % y
    elif isinstance(x, str) and isinstance(y, list):
        return x % tuple(y)
    elif isinstance(x, (ArcFunction, FunctionType)) and isinstance(y, list):
        return list(map(x, y))
    else:
        ArcError('value')

def _inc(n):
    if isinstance(n, (int, float)):
        return n + 1
    else:
        ArcError('value')

def _dec(n):
    if isinstance(n, (int, float)):
        return n - 1
    else:
        ArcError('value')

def _range(*args):
    if len(args) == 1:
        if isinstance(args[0], (list, str)):
            return len(args[0])
        start = 0
        stop = ArcEval(args[0])
        step = 1
    elif len(args) == 2:
        start, stop = args
        step = 1
    elif len(args) == 3:
        start, stop, step = args
    else:
        ArcError('arguments')
    return list(range(start, stop, step))

def _and(*args):
    if len(args) == 1:
        return all(args[0])
    else:
        return all(args)

def _line(prompt=""):
    return input(prompt)

def _numcast(n, tocast):
    try:
        return tocast(n)
    except ValueError:
        ArcError('value')

def _read(nbytes=-1):
    raw = sys.stdin.read(nbytes)
    if raw[-1] == '\n':
        final = raw[:-1]
    else:
        final = raw
    return final

def _index_slice(L, aslice):
    if len(aslice) == 1:
        return L[aslice[0]]
    elif len(aslice) == 2:
        start, stop = aslice
        step = 1
    elif len(aslice) == 3:
        start, stop, step = aslice
    else:
        ArcError('arguments')
    return L[start:stop:step]

def _virg(x, y):
    #print("Hello from virg, args:", x, y)
    if isinstance(x, (ArcFunction, FunctionType)):
        return list(filter(x, y))
    else:
        return x / y

def _print(*s):
    print(*s, end='')
    return ""

ArcBuiltins = {'+': _add,
               'p': _print,
               '%': _percent,
               ']': _inc,
               '[': _dec,
               '_': _range,
               '&': _and,
               '|': _or,
               'l': _line,
               '#': lambda n: _numcast(n, int),
               '.': lambda n: _numcast(n, float),
               't': True,
               'n': False,
               'q': _read,
               '=': lambda x,y: x==y,
               '<': lambda x,y: x<y,
               '>': lambda x,y: x>y,
               '*': lambda x,y: x*y,
               '-': lambda x,y: x-y,
               'pn': lambda *a: a[-1],
               'pg': lambda n, *a: a[n],
               '‰': lambda x,y: x%y == 0,
               '/': _virg,
               'r': functools.reduce,
               '^': lambda x,y: x**y,
               'b>': lambda x,y: x>>y,
               'b<': lambda x,y: x<<y,
               '1>': lambda x:x>>1,
               '1<': lambda x:x<<1,
               'b&': lambda x,y: x&y,
               'b|': lambda x,y: x|y,
               'b^': lambda x,y: x^y,
               'b~': lambda x: ~x,
               '~': lambda x: not x,
               'l?': lambda x: isinstance(x, list),
               's?': lambda x: isinstance(x, str),
               '#?': lambda x: isinstance(x, int),
               '.?': lambda x: isinstance(x, float),
               'n?': lambda x: isinstance(x, (int, float)),
               'zz': time.sleep,
               'st': time.strftime,}
            #    'add': lambda *a: _add,
            #    '-': lambda x,y: _sub,
            #    'sub': lambda x,y: _sub,
            #    '*': lambda *m: _mul,
            #    'mul': lambda *m: _mul,
            #    '/': lambda x,y: _div,
            #    'div': lambda x,y: _div,
            #    '//': lambda x,y: _floordiv,
            #    'floordiv': lambda x,y: _floordiv,
            #    '**': lambda x,y: _pow,
            #    'pow': lambda x,y: _pow,
            #    '~': lambda x: _bnot,
            #    'bnot': lambda x: _bnot,
            #    '!': _factorial,
            #    'factorial': _factorial,
            #    '#': int,
            #    'int': int,
            #    '.': float,
            #    'float': float,
            #    '&': _band,
            #    'band': _band,
            #    '|': _bor,
            #    'bor': _bor,
            #    '^': _bxor,
            #    'bxor': _bxor,
            #    '=': _eq,
            #    'eq': _eq,
            #    '\\': _reverse,
            #    'reverse': _reverse,
            #    '<': _lt,
            #    'lt': _lt,
            #    '>': gt,
            #    'gt': gt,
            #    '<=': lambda x,y: x<=y,
            #    'lteq': lambda x,y: x<=y,
            #    '>=': lambda x,y: x>=y,
            #    'gteq': lambda x,y: x>=y,
            #    '==': _stricteq,
            #    'stricteq': _stricteq,
            #    'lambda': ArcFunction,
            #    'F': ArcFunction,
            #    'sin': _sin,
            #    'cos': _cos,
            #    'tan': _tan}

ArcNamespace = {}
ArcNamespace.update(ArcBuiltins)
