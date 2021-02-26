import os
import sys

name = sys.argv[1] if len(sys.argv) > 1 else ""

for letter in "abcdef":
    os.system(f"pypy3 run.py {letter} {name}")