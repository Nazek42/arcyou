# Arcyóu's standard library. This is where all of the functions are stored.

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

from error import *
from types import FunctionType
import time
import operator
import math
import random
import sys
import functools

def is_num(thing):
    """Check if an object is a numeric type."""
    return isinstance(thing, (int, float))

def _add(*args):
    """Mathematical addition."""
    if len(args) == 1:
        return sum(args[0])
    else:
        return sum(args)

def _percent(x, y):
    """Modulo, string format, and map."""
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return x % y
    if isinstance(x, str):
        try:
            return x % tuple(y)
        except TypeError:
            return x % (y)
    if (isinstance(x, FunctionType) or is_ArcFunction(x)) and isinstance(y, list):
        return list(map(x, y))
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
        stop = args[0]
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

def _or(*args):
    if len(args) == 1:
        return any(args[0])
    else:
        return any(args)

def _line(prompt=""):
    return input(prompt)

def _icast(n):
    try:
        return int(n)
    except ValueError:
        ArcError('value')

def _fcast(n):
    try:
        return float(n)
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
    if len(aslice) == 2:
        start, stop = aslice
        step = 1
    elif len(aslice) == 3:
        start, stop, step = aslice
    else:
        ArcError('arguments')
    return L[start:stop:step]

def _virg(x, y):
    #print("x.__class__:", x.__class__)
    #print("Hello from virg, args:", x, y)
    #print(isinstance(x, FunctionType))
    #print(is_ArcFunction(x))
    if isinstance(x, FunctionType) or is_ArcFunction(x):
        return list(filter(x, y))
    else:
        return x / y

def _print(*s):
    print(*s)
    return ""

def _stackfilter(L, *funcs):
    if isinstance(funcs[0], list):
        funcs = funcs[0]
    return list(filter(lambda i: all(func(i) for func in funcs), L))

def _stackmap(L, *funcs):
    final = L[:]
    if isinstance(funcs[0], list):
        funcs = funcs[0]
    for func in funcs:
        final = map(func, final)
    return list(final)

ArcBuiltins = {'+': _add,
               'p': _print,
               '%': _percent,
               ']': _inc,
               '[': _dec,
               '_': _range,
               '&': _and,
               '|': _or,
               'l': _line,
               '#': _icast,
               '.': _fcast,
               't': True,
               'n': False,
               'q': _read,
               '=': operator.eq,
               '==': lambda x,y: x==y and type(x)==type(y),
               '<': operator.lt,
               '>': operator.gt,
               '*': lambda x,y: x*y,
               '-': operator.sub,
               'pn': lambda *a: a[-1],
               'pg': lambda n, *a: a[n],
               '/?': lambda x,y: x%y == 0,
               '/': _virg,
               '#/': operator.floordiv,
               'r': functools.reduce,
               '^': operator.pow,
               'b>': operator.rshift,
               'b<': operator.lshift,
               '1>': lambda x: x>>1,
               '1<': lambda x: x<<1,
               'b&': operator.and_,
               'b|': operator.or_,
               'b^': operator.xor,
               '~': operator.inv,
               '!': operator.not_,
               'l?': lambda x: isinstance(x, list),
               's?': lambda x: isinstance(x, str),
               '#?': lambda x: isinstance(x, int),
               '.?': lambda x: isinstance(x, float),
               'n?': is_num,
               'zz': time.sleep,
               'st': time.strftime,
               'z': lambda L1,L2: list(zip(L1,L2)),
               't': lambda L: list(zip(*L1)),
               'lc': str.lower,
               'uc': str.upper,
               'E': list.__contains__,
               '//': _stackfilter,
               '%%': _stackmap,
               'v': str.split,
               '\\': lambda s: s[::-1],
               'a': lambda L,x: L+[x],
               'i': lambda L,i,x: L[:i]+[x]+L[i:],
               'R': random.random,}

def is_ArcFunction(func):
    return repr(func.__class__) == "<class 'function.ArcFunction'>"
