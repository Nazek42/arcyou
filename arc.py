#!/usr/bin/env python3
# -*- coding=utf8 -*-

import sys
import os.path
import parsing
import function

usage = "Usage: arcyou path/to/source/code"

def main():
    if len(sys.argv) > 1:
        filename = os.path.abspath(sys.argv[1])
    else:
        print(usage)
        sys.exit()
    with open(filename) as file:
        code_raw = file.read()

    code = parsing.parse(code_raw)
    for cons in code:
        final = function.ArcEval(cons)
    print(final)

main()
