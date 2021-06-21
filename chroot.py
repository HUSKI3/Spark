from tarfile import open, is_tarfile
from subprocess import Popen, PIPE, call
from os import popen, system

from pathlib import Path
import distro



# Chroot for packaging
class chroot:


    def __init__(self):
        self.banana = "0"
        self.distro = {
            "name":distro.linux_distribution()[0],
            "version":distro.linux_distribution()[1],
            "release":distro.linux_distribution()[2],
            }
        self.home = str(Path.home())
        self.chroot_home = self.home+"/.spark_chroot"

    def cprint(self,msg=None,trace=None):
        if not trace and msg:
            print("[Chroot]",msg)
        else:
            print("[Chroot] Chroot trace:\n",trace)  

    def run_in_chroot(self,cmd):
        # Mount points
        run_command("sudo mount -t proc /proc proc".split(" "),self.chroot_home)
        run_command("sudo mount --rbind /sys sys".split(" "),self.chroot_home)
        run_command("sudo mount --rbind /dev dev".split(" "),self.chroot_home)

        # Enter chroot
        system(f'''cd $HOME/.spark_chroot && sudo chroot . /bin/bash -c "{cmd}" ''')
        self.close_chroot()

    def shell_chroot(self):
        # Mount points
        run_command("sudo mount -t proc /proc proc".split(" "),self.chroot_home)
        run_command("sudo mount --rbind /sys sys".split(" "),self.chroot_home)
        run_command("sudo mount --rbind /dev dev".split(" "),self.chroot_home)

        # Enter chroot
        run_command("sudo chroot . /bin/bash".split(" "),self.chroot_home)
        self.close_chroot()

    def build_chroot(self):
        run_command(f"mkdir -p .spark_chroot".split(" "),self.home)

        # Check distro
        if self.distro['name'] == "Ubuntu":

            # Create an ubuntu chroot
            run_command(f"sudo debootstrap --variant=buildd {self.distro['release']} .spark_chroot".split(" "),self.home)

        self.cprint("Done, validating...")

    def close_chroot(self):
        run_command("sudo umount sys dev".split(" "),self.home)





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


chroot = chroot()
chroot.build_chroot()
chroot.shell_chroot()