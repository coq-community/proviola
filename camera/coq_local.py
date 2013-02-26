""" Implements protocol for talking to local Coq installation.
"""
import shlex
import time
import signal
import pexpect

class Coq_Local(object):
  def __init__(self, coqtop="/usr/bin/coqtop"):
    """ Open a Coq process. 
      - coqtop: Location of coqtop executable.
      - timeout: How long to wait for coqtop to print to stdout. 
    """
    self.error = ""
    self._coqtop = None
    self._coqtop = pexpect.spawn(coqtop + ' -emacs')
    self._coqtop.setecho(False)
    
    # Clear Coq greeting.
    data = self._read_coq()
    if not data:
      print "Could not manage coq."

  def _read_coq(self):
    """ Read data from Coqtop. Read stdout after the  """
    self._coqtop.expect("<prompt>.*</prompt>")
    self.error = self._coqtop.after
    return self._clean(self._coqtop.before)

  def _clean(self, string):
    """ Clean a string. """
    string = string.lstrip()
    string = string.replace("\r", "")
    string = string.lstrip()
    return "".join([c for c in string if ord(c) != 253])
  
  def __del__(self):
    """ Clean up: stop Coq process. """
    if self._coqtop:
      self._coqtop.close()
    
  def send(self, command):
    """ Send data to Coqtop, returning the result. """
    self._coqtop.sendline(command)
    return self._read_coq()
   
  def interrupt(self):
    self._coqtop.kill(signal.SIGINT)
