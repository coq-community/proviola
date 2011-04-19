""" Implements protocol for talking to local Coq installation.
"""

import subprocess
import time
# The solutions here are *Nix-specific.
import fcntl, os 

class Coq_Local(object):
  def __init__(self, coqtop = "/usr/bin/coqtop"):
    """ Open a Coq process. 
      - coqtop: Location of coqtop executable.
      - timeout: How long to wait for coqtop to print to stdout. 
    """
    self._coqtop = subprocess.Popen(coqtop.split(),
                                    stdin  = subprocess.PIPE,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
    fcntl.fcntl(self._coqtop.stdout, fcntl.F_SETFL, os.O_NONBLOCK) 
    fcntl.fcntl(self._coqtop.stderr, fcntl.F_SETFL, os.O_NONBLOCK)
    
    # Clear Coq greeting.
    data = self._read_coq()
    if not data:
      print "Could not manage coq."

  def _read_coq(self):
    """ Read data from Coqtop. Read stdout after the  """
    error = ""
    while not error:
      try:
        error = self._coqtop.stderr.read()
      except IOError:
        time.sleep(.1)
        
    try:
      output = self._coqtop.stdout.read()
    except IOError:
      output = ""
    
    return output
    
  def __del__(self):
    """ Clean up: stop Coq process. """
    self._coqtop.terminate()
    
  def send(self, command):
    """ Send data to Coqtop, returning the result. """
    self._coqtop.stdin.write(command + "\n")
    self._coqtop.stdin.flush()
    return self._read_coq()
    