# Arcyou's function library. This handles the actual execution of code.

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
from collections import Hashable
from arcstdlib import ArcBuiltins, _index_slice, is_num

class ArcFunction:
    """
A function in live code is represented by this.
    """
    def __init__(self, params, body):
        #print("Hello from function constructor, params:", params)
        self.params = params[:]
        self.body = body[:]
    def __repr__(self):
        return "F(%s)" % ' '.join(self.params)
    def __call__(self, *args):
        global nsset, nspop
        #print("ArcFunction's args:", args)
        nsset(zip(self.params, args))
        # Fixpoint
        nsset([ ('$', ArcFunction(self.params, self.body)) ])
        result = ArcEval(self.body)
        for param in self.params:
            try:
                nspop(param)
            except KeyError:
                pass
        try:
            nspop('$')
        except KeyError:
            pass
        return result

def ArcEval(cons):
    """
The core of Arcyou, a work of intricate recursion.
*This* is what executes code.
Arguments: cons <-- A single Arcyou cell
Returns: the result of evaluating that cell. The only thing that is guaranteed
is that you won't get another cell.
    """
    #print("cons:", cons)
    # Is it an atom?
    global nsset, nsget
    if is_num(cons):
        return cons
    if is_string_literal(cons):
        return cons[1:-1]
    if isinstance(cons, Hashable):
        #print("Hello from hashable")
        try:
            lookup = nsget(cons)
            #print("ns:", lookup)
            if lookup==None and type(lookup)==type(None):
                return cons
            return lookup
        except:
            raise

    if not cons: # empty list?
        return None

    # Is it a special form?
    #print("Hello from special form handler")
    func = cons[0]
    # If
    if func == '?':
        cond = ArcEval(cons[1])
        return ArcIf(cond, cons[2:4])
    # While
    if func == '@':
        return ArcWhile(cons[1:3])
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
        nsset([ (cons[1], value) ])
        return value
    # Quote
    if func == '\'':
        result = [ArcEval(i) if isinstance(i, list) else i for i in cons[1:]]
        return result

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
    if isinstance(funcr, (str, list)):
        result = _index_slice(funcr, arguments)
    elif arguments != []:
        result = funcr(*arguments)
    else:
        result = funcr()
    #print("result:", result)
    return result

def is_string_literal(thing):
    """Check if a symbol is actually a string literal."""
    global sw, ew
    return isinstance(thing, str) and sw(thing, '"') and ew(thing, '"')

def ArcIf(cond, cases):
    """If-statement."""
    iftrue, iffalse = cases
    if cond:
        return ArcEval(iftrue)
    else:
        return ArcEval(iffalse)

def ArcFor(symbol, iterator, body):
    """For loop/listcomp."""
    global nsset, nspop
    result = []
    rappend = result.append
    for item in iterator:
        nsset([ (symbol, item) ])
        rappend(ArcEval(body))
    try:
        nspop(symbol)
    except KeyError:
        pass
    return result

def ArcWhile(args):
    """While loop/incredibly abstract comprehension."""
    cond, body = args
    result = []
    rappend = result.append
    while ArcEval(cond):
        rappend(ArcEval(body))
    return result

ArcNamespace = {}
ArcNamespace.update(ArcBuiltins)
nsget = ArcNamespace.get
nsset = ArcNamespace.update
nspop = ArcNamespace.pop

sw = str.startswith
ew = str.endswith
