#!/usr/bin/python3

from tarfile import open, is_tarfile
from subprocess import Popen, PIPE, call
from os import popen, system
from glob import glob
from json import load

class packager():
    """Packs/depacks files in .spk format

    Args:
        file (string): File/ Folder to be packed/unpacked
        pkg (bool, optional): If the file needs to be depacked. Defaults to True.
    """


    def __init__(self, file, pkg=True):
        pkgname = "{}.spk".format(file)

        try:
            # So this packages a folder into .spk
            # folder --> .spk if pkg is true else .spk --> folder

            if not pkg:
                self.dpkging(pkgname, file)
            elif checkFolder(file) and pkg:
                self.pkging(file, pkgname)
            else:
                print("ERR: No such file in directory")

        except IOError as err:
            print("ERR: Package not found", err)

    def dpkging(self, pkgname, file):
        # Unpacking (folder not required)
        system('tar -zxvf {}'.format(pkgname))

        print("running the package installer")
        print(run_command(["bash", "install.sh"], file))

        metadata = LoadMeta(file)

    def pkging(self, file, pkgname):
        # Packaging (requires folder and validation)
        for dir in ['bin', 'fs', 'libs', 'deps', 'install.sh', 'metadata.json']:
            if not checkFolder(f'{file}/{dir}'):
                print("ERR: Invalid package")
                quit()
        print("packaging")
        system('tar -czf {} {}'.format(pkgname, file))


def checkFolder(file):
    if glob(file):
        return True
    else:
        return False




# daemon? is that what this is called?
def run_command(command, dir):
    """A daemon, runs the command and gives output\n
    Will parse stuff

    Args:
        command (string): What command to run

    Returns:
        String: Realtime output to the inputted command
    """

    process = Popen(command, stdout=PIPE, cwd=dir)
    alive = True
    while alive:
        output = process.stdout.readline()      
        print(output.strip().decode("utf-8")) if output else None
        alive = process.poll() is None

    rc = process.poll()
    return rc


def LoadMeta(file):
    with open(f'{file}/metadata.json') as f:
        metadata = load(f)
