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

        metadata = ezconfig()
        metadata.read('pain.json')
        print(metadata.datajson)

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




# 
# ==============================================
#                     Ezconf
# ==============================================
#

import json
import re



class ezconfig:

  def __init__(self):
    self.filename = ""
    self.datajson = None

  def read(self,filename):
    """
    Reads the config file and saves the values
    :return: 
    """
    try:
      with open(str(filename),"r") as f:
        data = f.read()
        #check if the loaded file is json
        try:
          datajson = json.loads(data)
        except Exception as e:
          print('could not load '+str(filename)+', add a basic entry to the config like {"name":"Example"}. Python error: '+str(e))
          return 1
        self.datajson = datajson
        self.filename = filename
        f.close()
        return 0
    except:
      return 1

  def get(self,var,*args):
    """
    Return a variable
    :param var: variable to get
    :return var_val:
    """

    # colours
    fail = "\u001b[31m"
    reset = "\u001b[0m"

    #update datajson
    self.read(self.filename)
    try:
      var_val = self.datajson[str(var)]
      if bool(args)!=False:
        p = re.compile('(?<!\\\\)\'')
        var_val = p.sub('\"', str(var_val))
        return json.loads(str(var_val))[str(args[0])]
    except Exception as e:
      print(fail+"[1] "+reset+ "could not get variable ["+str(var)+"] does it exist in "+self.filename+"?\nPython error: "+str(e))
      print(self.datajson)
      quit()
    if var_val == None:
      print(fail+"[2] "+reset+ "could not get variable ["+str(var)+"]. It equals to None, is there a python problem?")
      quit()
    else:
      return var_val
  
  def update(self,var,*args):
    """
    Update a variable
    :param var: variable to update
    """
    #update datajson
    self.read(self.filename)
    try:
      self.datajson[str(var)] = str(args[0])
    except Exception as e:
      merrors.error("could not update variable, does it exist? Did you parse a new value? Python error: "+str(e))
    jsonFile = open(str(self.filename), "w+")
    jsonFile.write(json.dumps(self.datajson))
    jsonFile.close()

  def update_all(self):
    """
    Update all
    """
    jsonFile = open(str(self.filename), "w+")
    jsonFile.write(json.dumps(self.datajson))
    jsonFile.close()

  def pretty(self):
    """
    Return pretty print
    :return prettyprint:
    """
    #update datajson
    self.read(self.filename)
    try:
      return json.dumps(self.datajson, indent=4, sort_keys=True)
    except Exception as e:
      merrors.error("could not pretty print, did you load the config? Python error: "+str(e))
      quit()

  def nested(self,main,name,var):
    self.read(self.filename)
    tmp = []
    try:
      old_nested = self.get(str(main))
    except Exception as e:
      merrors.error("could not create a nested value, does the main value exist? Python error: "+str(e))
      quit()
    for elem in old_nested:
      tmp.append(elem)
    tmp.append({str(name):str(var)})
    self.datajson[str(main)] = tmp
    file = open(str(self.filename), "w")
    json.dump(self.datajson,file)
    file.close()

  def add(self,name,var):
    file = open(str(self.filename), "w")
    self.datajson[str(name)] = str(var)
    json.dump(self.datajson,file)
    file.close()
