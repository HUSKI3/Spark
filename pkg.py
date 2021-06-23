#!/usr/bin/python3

from tarfile import open as topen, is_tarfile

from subprocess import Popen, PIPE, call, check_output, run
from os import popen, system, path
from glob import glob
from json import load, loads

path.dirname(path.realpath(__file__))

# TODO(Kunal, Artur): Get install thing working better with parsed outputs and all

class packager():
    """Packs/depacks files in .spk format

    Args:
        file (string): File/ Folder to be packed/unpacked
        pkg (bool, optional): If the file needs to be depacked. Defaults to True.
    """


    def __init__(self, file, pkg=True, meta=False):
        pkgname = "{}.spk".format(file)

        try:
            # So this packages a folder into .spk
            # folder --> .spk if pkg is true else .spk --> folder
            if meta:
                self.read_meta(pkgname, file)
                return

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
        popen('tar -zxvf {}'.format(pkgname)).read()

        print("running the package installer")
        print(run_command(["bash", "install.sh"], file))


    def read_meta(self,pkgname,file):
        # tar xfO nano.spk nano/metadata.json | cat
        result = run(f"tar xfOs {pkgname} {file}/metadata.json | cat".split(" "), stdout=PIPE)
        result = result.stdout.decode('utf-8')
        result = loads(result)
        files = run(f"tar tf {pkgname} ".split(" "), stdout=PIPE)
        files = files.stdout.decode('utf-8')
        #print(check_output(f"tar xfO {pkgname} {file}/metadata.json | cat".split(" ")))
        print(f"""
Package info:
Name: {result['package-data'][0]['name']}
Size: {result['package-data'][0]['size']}
Depends on: {result['package-data'][0]['depends']}
Build instructions: {result['package-data'][0]['build']}
Install instructions: {result['package-data'][0]['build']}
Files in package: 
{files}
""")

    def pkging(self, file, pkgname):
        # Packaging (requires folder and validation)
        for dir in ['bin', 'fs', 'libs', 'deps', 'install.sh', 'metadata.json']:
            if not checkFolder(f'{file}/{dir}'):
                print("ERR: Invalid package")
                quit()
        print("packaging")
        popen('tar -czf {} {}'.format(pkgname, file)).read()


def checkFolder(file):
    return True if glob(file) else False


# runs install.sh
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
        return metadata