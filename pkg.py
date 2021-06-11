from subprocess import Popen

with Popen("bash test.sh").read() as s:
    print(s)
