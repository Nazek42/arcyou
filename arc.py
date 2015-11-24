#!/usr/bin/env python3
# -*- coding=utf8 -*-
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
# along with Arcyóu.  If not, see <http://www.gnu.org/licenses/>.

VERSION = "a1"

import sys
import os.path
import parsing
import function
from cmd import Cmd

def main():
    if len(sys.argv) > 1:
        filename = os.path.abspath(sys.argv[1])
    else:
        repl()
    with open(filename) as file:
        code_raw = file.read()

    code = parsing.parse(code_raw)
    for cons in code:
        final = function.ArcEval(cons)
    print(final)

def repl():
    function.ArcNamespace['bye'] = lambda: print("Bye.")
    try:
        ArcRepl().cmdloop()
        sys.exit()
    except EOFError:
        print("Bye.")
        sys.exit()

class ArcRepl(Cmd):
    intro = """Arcyóu version {0}. Copyright (C) 2015 Benjamin Kulas.
This program comes with ABSOLUTELY NO WARRANTY; for details see the source code or the GNU General Public License version 3.

Type (bye) to exit.
    """.format(VERSION)
    use_rawinput = False
    prompt = "(油:0)> "
    fprompt = "(油:%d)> "
    n = 0
    def precmd(self, line):
        return parsing.parse(line)[0]
    def onecmd(self, cons):
        return print(function.ArcEval(cons))
    def postcmd(self, stop, cons):
        self.n += 1
        self.prompt = self.fprompt % self.n
        return cons == ['bye']


main()
