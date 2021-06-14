#!/usr/bin/python3

from tarfile import open, is_tarfile
from subprocess import Popen, PIPE, call

class packager():
    """Packs/depacks files in .spk format

    Args:
        file (string): File/ Folder to be packed/unpacked
        dpkg (bool, optional): If the file needs to be depacked. Defaults to True.
    """

    def __init__(self, file, dpkg=True):
        pkgname = "{}.spk".format(file)

        try:
            # So this packages a folder into .spk
            # TODO Add checks to check the validity of the folder to be a package
            if not dpkg:
                call(['tar', '-czf', pkgname, file])
            
            # unpacks .spk into a folder
            else:
                spk = open('{}.spk'.format(file), ('r' if dpkg else 'w')) if is_tarfile(('{}.spk'.format(file))) else print("ERR: Not a valid package")
                spk.extractall()

                call(['tar', '-zxvf', pkgname])

                # Then it does all the procedures in install.sh

                    
        except IOError:
            print("ERR: Package not found")


# daemon? is that what this is called?
def run_command(command):
    """A daemon, runs the command and gives output\n
    Will parse stuff

    Args:
        command (string): What command to run

    Returns:
        String: Realtime output to the inputted command
    """

    process = Popen(command, stdout=PIPE)
    alive = True
    while alive:
        output = process.stdout.readline()      
        print(output.strip().decode("utf-8")) if output else None
        alive = process.poll() is None

    rc = process.poll()
    return rc


# run_command(["bash", "./package/install.sh"])
