import parsing
import function
import pickle
import os.path

def ArcCompile(ipath, opath=""):
    path = os.path.abspath(ipath)
    if os.path.isfile(path):
        with open(path, 'rt') as ifile:
            code_raw = ifile.read()
    else:
        return 1
    code = parsing.parse(code_raw)

    old_ns = {symbol: value for symbol, value in function.ArcNamespace.items()}
    for cons in code:
        function.ArcEval(cons)
    diff = {symbol: value for symbol, value in function.ArcNamespace.items() if symbol not in old_ns}

    if not opath:
        # For a filename like 'math.arc.foobar', this gives 'math.ayc'
        opath = os.path.basename(path).split('.')[0] + '.ayc'
    opath = os.path.abspath(opath)
    with open(opath, 'wb') as ofile:
        pickle.dump(diff, ofile, protocol=4)
    return 0
