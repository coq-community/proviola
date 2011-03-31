""" Implements protocol for talking to local Coq installation.
"""

import subprocess
import select
# The solutions here are *Nix-specific.
import fcntl, os 

class Coq_Local(object):
  def __init__(self, coqtop = "/usr/bin/coqtop"):
    """ Open a Coq process. """
    self._coqtop = subprocess.Popen(coqtop,
                                    stdin  = subprocess.PIPE,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)

    print fcntl.fcntl(self._coqtop.stdout, fcntl.F_SETFL, os.O_NONBLOCK) 
    
    # Clear Coq greeting.
    select.select([self._coqtop.stdout], [], [])
    self._coqtop.stdout.readline()
    
    
  
  def __del__(self):
    """ Clean up: stop Coq process. """
    self._coqtop.terminate()
    
  def send(self, command):
    self._coqtop.stdin.write(command + "\n")
    self._coqtop.stdin.flush()
    select.select([self._coqtop.stdout], [], [])
    return self._coqtop.stdout.read()