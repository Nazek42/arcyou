import sys
import os.path
import parsing
import function

def main():
    if len(sys.argv) > 1:
        filename = os.path.abspath(sys.argv[1])
    else:
        print(usage)
        sys.exit()
    with open(filename) as file:
        code_raw = file.read()

    code = parsing.parse(code_raw)
    if len(code) == 1:
        code = [code]
    for cons in code:
        final = function.ArcEval(cons)
    print(final)

main()
