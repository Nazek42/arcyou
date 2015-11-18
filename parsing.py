import errors

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

def parse(code):
    tokens = tokenize(code)
    return clean(code)
