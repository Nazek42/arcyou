# Arcyou's function library.

from types import FunctionType
from error import *

ArcBuiltins = {}
ArcNamespace = {}

class ArcFunction:
    def __init__(self, params, body):
        self.params = params[:]
        self.body = body[:]
    def __call__(self, args):
        print("Hello from funcx.__call__:",args)
        global ArcNamespace
        for param, arg in zip(self.params, map(ArcEval,args)):
            print(param,arg)
            ArcNamespace[param] = arg
        ArcNamespace['$'] = self
        result = ArcEval(self.body)
        print("ArcNamespace:",ArcNamespace)
        for param in self.params:
            ArcNamespace.pop(param)
        ArcNamespace.pop('$')
        return result

def ArcEval(cons):
    """
Arcyou's eval function.
    """
    print("cons:",cons)
    global ArcNamespace
    if isinstance(cons, str):
        if cons.startswith('"') and cons.endswith('"'):
            return cons
        else:
            return ArcNamespace[cons]
    if not isinstance(cons, list):
        return cons
    if cons == []:
        return []
    func = cons[0]
    args = cons[1:]
    if func in ('if', '?'):
        cond = ArcEval(args[0])
        return ArcIf(cond, *args[1:])
    elif func in ('while', '@'):
        return ArcWhile(*args)
    elif func in ('for', 'f'):
        symbol = args[0]
        iterator = ArcEval(args[1])
        body = args[2]
        return ArcFor(symbol, iterator, body)
    elif func in ('quote', '\''):
        if len(args) == 1:
            return ArcEval(args[0])
        else:
            return args
    elif func in ('set', ':'):
        symbol = args[0]
        value = ArcEval(args[1])
        ArcNamespace[symbol] = value
        return value
    elif func in ('lambda', 'F'):
        print("Hello from lambda handler")
        params = args[0]
        body = args[1]
        return ArcFunction(params, body)
    elif isinstance(func, list):
        funcx = ArcEval(func)
        if isinstance(funcx, ArcFunction):
            print(func)
            return funcx(args)
        else:
            return funcx
    elif func in ArcNamespace.keys():
        funcx = ArcNamespace[func]
        print("args:",args)
        resolved_args = list(map(ArcEval, args))
        print("resolved_args:",resolved_args)
        if isinstance(funcx, ArcFunction):
            return funcx.execute(resolved_args)
        elif isinstance(funcx, FunctionType):
            return funcx(*resolved_args)
        else:
            ArcError('expected-function')
    else:
        print("Here:", func)

def ArcIf(cond, iftrue, iffalse):
    if cond:
        return ArcEval(iftrue)
    else:
        return ArcEval(iffalse)

def ArcFor(symbol, iterator, body):
    print("Hello from for")
    global ArcNamespace
    result = []
    for item in iterator:
        ArcNamespace[symbol] = item
        result.append(ArcEval(body))
    if symbol in ArcNamespace:
        ArcNamespace.pop(symbol)
    return result

def ArcWhile(cond, body):
    result = []
    while ArcEval(cond):
        result.append(ArcEval(body))
    return result

def _add(*args):
    if len(args) == 1:
        return sum(args[0])
    elif all(map(lambda x:isinstance(x,list), args)):
        return sum(args, [])
    else:
        return sum(args)

def _print(*iargs):
    args = []
    for arg in iargs:
        if isinstance(arg, str):
            if arg.startswith('"') and arg.endswith('"'):
                args.append(arg[1:-1])
        else:
            args.append(arg)
    print(*args)
    return ""

def _percent(x, y):
    print("Hello from percent")
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return x % y
    elif isinstance(x, str) and isinstance(y, list):
        return x % tuple(y)
    elif isinstance(x, (ArcFunction, FunctionType)) and isinstance(y, list):
        return list(map(x, y))
    else:
        ArcError('value-error')

def _inc(n):
    if isinstance(n, (int, float)):
        return n + 1
    else:
        ArcError('value-error')

def _dec(n):
    if isinstance(n, (int, float)):
        return n - 1
    else:
        ArcError('value-error')

def _range(*args):
    print("Hello from range")
    if len(args) == 1:
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
    print("SSS:",start, stop, step)
    return list(range(start, stop, step))

def _and(*args):
    print("Hello from and")
    if len(args) == 1:
        return all(args[0])
    else:
        return all(args)

def _line(prompt=""):
    return input(prompt)

def _int(n):
    return int(n)


ArcBuiltins = {'+': _add,
               'p': _print,
               '%': _percent,
               ']': _inc,
               '[': _dec,
               '_': _range,
               '&': _and,
               'l': _line,
               '#': _int}
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
