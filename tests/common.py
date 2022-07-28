import os
import sys

def importPath():
    root = os.path.dirname(os.getcwd())
    sys.path.append(root)