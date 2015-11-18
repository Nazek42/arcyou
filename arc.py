import sys
import os.path
import functools
import math

ArcGlobals = {'+': lambda *a: _add,
              'add': lambda *a: _add,
              '-': lambda x,y: x-y,
              'sub': lambda x,y: x-y,
              '*': lambda *m: _mul,
              'mul': lambda *m: _mul,
              '/': lambda x,y: x/y,
              'div': lambda x,y: x/y,
              '//': lambda x,y: x//y,
              'floordiv': lambda x,y: x//y,
              '**': lambda x,y: x**y,
              'pow': lambda x,y: x**y,
              '~': lambda x: ~x,
              'bnot': lambda x: ~x,
              '!': math.factorial,
              'factorial': math.factorial,
              '#': int,
              'int': int,
              ';': float,
              'float': float,
              '&': lambda x,y: x&y,
              'band': lambda x,y: x&y,
              '|': lambda x,y: x|y,
              'bor': lambda x,y: x|y,
              '^': lambda x,y: x^y,
              'bxor': lambda x,y: x^y,
              '=': lambda *e: e[0].count(e[0][0])==len(e[0]) if isinstance(e[0],list) else e.count(e[0])==len(e),
              'eq': lambda *e: e[0].count(e[0][0])==len(e[0]) if isinstance(e[0],list) else e.count(e[0])==len(e),
              '\\': lambda l: l[::-1],
              ':': lambda i,v: ArcGlobals[i]=v,
              'set': lambda i,v: ArcGlobals[i]=v,
              '<': lambda x,y: x<y,
              'lt': lambda x,y: x<y,
              '>': lambda x,y: x>y,
              'gt': lambda x,y: x>y,
              '<=': lambda x,y: x<=y,
              'lteq': lambda x,y: x<=y,
              '>=': lambda x,y: x>=y,
              'gteq': lambda x,y: x>=y,
              '==': lambda x,y: x==y and type(x) == type(y)
              'stricteq': lambda x,y: x==y and type(x) == type(y)
              'λ': ArcFunction,
              'lambda': ArcFunction,
              'sin': math.sin,
              'cos': math.cos,
              'tan': math.tan,







def main():
    if len(sys.argv) > 1:
        filename = os.path.abspath(sys.argv[1])
    else:
        print(usage)
        sys.exit()
    with open(filename) as file:
        code_raw1 = file.read()

    default_recursion_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(code.count('(') + 100) # Making sure we can parse it
    code_raw2 = parse(code_raw)
    code = clean(code_raw2)
    sys.setrecursionlimit(default_recursion_limit) # Stay safe, kids

def clean(icode):
    code = icode[:]
    i = 0
    temp = ""
    print('\n',code)
    print(len(code))
    while i< len(code):
        print(i)
        item = code[i]
        if isinstance(item, str):
            if item == ' ':
                if temp != "":
                    try:
                        code[i] = int(temp)
                    except ValueError:
                        try:
                            code[i] = float(temp)
                        except ValueError:
                            code[i] = temp
                    temp = ""
                else:
                    code.pop(i)
                    i -= 1
            else:
                temp += code.pop(i)
                i -= 1
        else: # it's a list
            code[i] = clean(item[:])
        i += 1
    if temp != "":
        code.append(temp)
    return code

def _add(*args):
