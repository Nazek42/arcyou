# Arcyou's parsing library. Handles comment removal, string literals, omitted
# close-parens, and abstract syntax tree creation.

import errors
from re import sub, MULTILINE
from sys import getrecursionlimit, setrecursionlimit

ESCAPES = {'n': '\n',
           't': '\t',
           'v': '\v',
           'a': '\a',
           'b': '\b',
           'f': '\f',
           'r': '\r'}


def parse(code):
    """
The top-level function for this library, the only one that should be called
externally. It applies all of the above functions in sequence to some raw
code that it is passed.
    """
    old_rl = getrecursionlimit()
    setrecursionlimit(code.count('(') + 50) # This should be comfortable
    stage1 = remove_comments(code)
    stage2, literals = extract_string_literals(stage1)
    stage3 = add_close_parens(stage2)
    stage4 = tokenize(stage3)
    stage5 = clean(stage4)
    stage6 = insert_string_literals(stage5, literals)
    setrecursionlimit(old_rl)
    return stage6

def remove_comments(code):
    """
Remove all comments from a program.
    """
    return sub(r";.*$", '', code, flags=MULTILINE)

def extract_string_literals(code):
    """
Deal with string literals inside an Arcyou program. Also handles Unicode
escapes, ASCII escapes, and a few other standard ones.
    """
    code = code.replace('\x02', '')
    final = ""
    in_string = False
    literals = []
    pointer = 0
    index = 0
    temp = ""
    while pointer < len(code):
        char = code[pointer]
        if in_string:
            if char == '\\':
                if code[pointer+1] == 'u':
                    # Handle Unicode escapes
                    temp += chr(int(code[pointer+2:pointer+6], 16))
                    pointer += 5
                elif code[pointer+1] == 'x':
                    # Handle \x.. escapes
                    temp += chr(int(code[pointer+2:pointer+4], 16))
                    pointer += 3
                else:
                    # Handle all other escapes
                    if code[pointer+1] in ESCAPES:
                        temp += ESCAPES[code[pointer+1]]
                    else:
                        temp += code[pointer+1]
                    pointer += 1
            elif char == '\"':
                if temp in literals:
                        final += '\x02' + chr(literals.index(temp))
                else:
                    literals.append(temp)
                    if index <= 0xFFFF:
                        final += '\x02' + chr(index)
                    else:
                        errors.ArcError('strmax')
                in_string = False

            else:
                temp += char
        else:
            if char == '\"':
                in_string = True
            else:
                final += char
        pointer += 1
    return final, literals

def add_close_parens(code):
    """
This is a feature while allows one to strip a fair amount of bytes off their
program. Any closing parentheses at the end of the program can be omitted. This
function adds them back in for parsing purposes.
    """
    return code + ')'*(code.count('(') -  code.count(')'))

def tokenize(code):
    """
Split the code into indiviual-character tokens in a nested list.
 Example:
"(eq (+ x 1) y)" -> ['e','q',' ', ['+',' ','x',' ','1'],' ','y']
    """
    def parsehelper(level=0):
        try:
            token = next(tokens)
        except StopIteration:
            if level != 0:
                errors.ArcError("missing-)")
            else:
                return []
        if token == ')':
            if level == 0:
                errors.ArcError("missing-(")
            else:
                return []
        elif token == '(':
            return [parsehelper(level+1)] + parsehelper(level)
        else:
            return [token] + parsehelper(level)
    tokens = iter(code)
    return parsehelper()

def clean(icode):
    """
Clean up the output from tokenize(). Also converts numeric literals.
Example:
tokenize("(eq (+ x 1) y)") -> ['eq',('+','x',1),'y']
    """
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

def insert_string_literals(icode, literals):
    code = icode[:]
    i = 0
    while i < len(code):
        item = code[i]
        if isinstance(item, str) and str.startswith('\x02'):
            code[i] = '"' + literals[ord(item[1])] + '"'
        elif isinstance(item, list):
            code[i] = insert_string_literals(item, literals)
        i += 1
