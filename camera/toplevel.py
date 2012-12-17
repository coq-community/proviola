""" Toplevel emulation from python. """
# The solutions here are *Nix-specific.
import subprocess
import fcntl, os

class Toplevel(object):
  def __init__(self, arguments):
    self._process = subprocess.Popen(arguments, 
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE)

    fcntl.fcntl(self._process.stdout, fcntl.F_SETFL, os.O_NONBLOCK) 
    fcntl.fcntl(self._process.stderr, fcntl.F_SETFL, os.O_NONBLOCK)

    self.stderr = self._process.stderr
    self.stdout = self._process.stdout
    self.stdin = self._process.stdin

  def kill(self):
    if self._process:
      self._process.kill()

