#!/usr/bin/python3

from tarfile import open, is_tarfile
from subprocess import Popen, PIPE

class packager():
    def __init__(self, file, dpkg=True):
        try:
            spk = open('{}.spk'.format(file), ('r' if dpkg else 'w')) if is_tarfile(('{}.spk'.format(file))) else print("ERR: Not a valid package")
            spk.extractall()

            # Then it does all the procedures in install.sh

        except IOError:
            print("ERR: Package not found")


# daemon? is that what this is called?
def run_command(command):
    process = Popen(command, stdout=PIPE)
    alive = True
    while alive:
        output = process.stdout.readline()      
        print(output.strip().decode("utf-8")) if output else None
        alive = process.poll() is None

    rc = process.poll()
    return rc


# run_command(["bash", "./package/install.sh"])
