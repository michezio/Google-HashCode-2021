import os

# change the python_exec to use different python interpreters
python_exec = "python"
# change the path to the folder containing the input files
path = "input/"

for name in ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]:
    os.system(f"{python_exec} solve.py {path}{name}")