""" Implements protocol for talking to local Coq installation.
"""

import subprocess, shlex
import time
# The solutions here are *Nix-specific.
import fcntl, os 

class Coq_Local(object):
  def __init__(self, coqtop = "/usr/bin/coqtop"):
    """ Open a Coq process. 
      - coqtop: Location of coqtop executable.
      - timeout: How long to wait for coqtop to print to stdout. 
    """
    self.error = ""
    self._coqtop = subprocess.Popen(shlex.split(coqtop) + ["-emacs"],
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
    output = ""

    while not error or not (error.find("</prompt>") >= 0):
      try:
        error = self._coqtop.stderr.read()
      except IOError:
        # Unclog stdout.
        try:
          output += self._clean(self._coqtop.stdout.read())
        except IOError:
          pass

        time.sleep(.1)

    self.error= error

    stop = False
    while not stop:
      try:
        output += self._clean(self._coqtop.stdout.read())
      except IOError:
        stop = True
    
    return output

  def _clean(self, string):
    """ Clean a string. """
    return "".join([c for c in string if ord(c) != 253])
  
  def __del__(self):
    """ Clean up: stop Coq process. """
    self._coqtop.terminate()
    
  def send(self, command):
    """ Send data to Coqtop, returning the result. """
    self._coqtop.stdin.write(command + "\n")
    self._coqtop.stdin.flush()

    return self._read_coq()
    
