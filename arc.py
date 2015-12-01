#!/usr/bin/env python3
# -*- coding=utf-8 -*-
#
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
# along with Arcyóu, located in the file `LICENSE'. If not, see
# <http://www.gnu.org/licenses/>.

VERSION = "v0.1a"

import sys
import os
import parsing
import function
from cmd import Cmd
import cProfile
try:
    import readline
    have_readline = True
except ImportError:
    have_readline = False

def main():
    load('math.arc')
    if len(sys.argv) == 2:
        filename = os.path.abspath(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] in ('-c', '--compile'):
        comp.ArcCompile(sys.argv[2])
        sys.exit()
    else:
        repl()
    with open(filename) as file:
        code_raw = file.read()

    ast = parsing.parse(code_raw)
    function.nsset([('¢', ast)])
    for cons in ast:
        final = function.ArcEval(cons)
    print(final)

def load(path):
    with open(path, 'rt') as file:
        code_raw = file.read()
    ast = parsing.parse(code_raw)
    for cons in ast:
        if cons:
            function.ArcEval(cons)

def repl():
    function.nsset([('bye', lambda: print("Bye."))])
    if not have_readline:
        print("\nWARNING: GNU readline functionality may not be available.")
    try:
        ArcRepl().cmdloop()
    except KeyboardInterrupt:
        function.nsget('bye')()
    sys.exit()

class ArcRepl(Cmd):
    intro = """Arcy\u00F3u version {0}. Copyright (C) 2015 Benjamin Kulas.
This program comes with ABSOLUTELY NO WARRANTY; for details see the source code or the GNU General Public License version 3.

Type (bye) or press Ctrl-C to exit.
    """.format(VERSION)
    use_rawinput = True
    fprompt = "(\u6CB9:%d)> "
    n = 0
    prompt = fprompt % n
    def precmd(self, line):
        if line:
            return parsing.parse(line)[0]
    def onecmd(self, cons):
        if cons:
            print(function.ArcEval(cons))
        return ""
    def postcmd(self, stop, cons):
        self.n += 1
        self.prompt = self.fprompt % self.n
        return cons == ['bye']

if len(sys.argv) > 1 and 'p' in sys.argv[1]:
    sys.argv.pop(0)
    cProfile.run("main()")
else:
    main()
