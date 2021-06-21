#!/usr/bin/python3

from tarfile import open, is_tarfile
from subprocess import Popen, PIPE, call
from os import popen, system

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
            # TODO(Kunal): Add checks to check the validity of the folder to be a package
            

            # asks user for preference
            # comment does not explain much
            # basically next line packs
            
            # folder --> .spk if pkg is true else .spk --> folder
            if not pkg:
                # Unpacking (file not required)
                system('tar -zxvf {}'.format(pkgname))
                
                print("running the package installer")
                print(run_command(["bash", "install.sh"], file))
            elif checkFolder(file) and pkg:
                print("packaging")
                # Packaging (requires file)
                system('tar -czf {} {}'.format(pkgname, file))
            else:
                print("ERR: No such file in directory")

        except IOError as err:
            print("ERR: Package not found", err)

        


def checkFolder(file, baseDir=""):
    if not baseDir:
        return 'y' in popen(f'if test -d {file}; then echo y; fi').read()
    else:
        return 'y' in popen(f'if test -d {baseDir}/{file}; then echo y; fi').read()

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


# run_command(["bash", "./package/install.sh"])
