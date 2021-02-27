import os

# change the python_exec to use different python interpreters
python_exec = "python"

for name in ["a.txt", "b.txt", "c.txt", "d.txt", "e.txt", "f.txt"]:
    os.system(f"{python_exec} solve.py {name}")