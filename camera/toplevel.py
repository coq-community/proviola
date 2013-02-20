""" Toplevel emulation from python. """
# The solutions here are *Nix-specific.
import subprocess32 as subprocess
import fcntl, os

class Toplevel(subprocess.Popen):
  def __init__(self, *args, **kargs):
    kargs['stdin'] = subprocess.PIPE
    kargs['stderr'] = subprocess.PIPE
    kargs['stdout'] = subprocess.PIPE
    kargs['close_fds'] = True
    super(Toplevel, self).__init__(*args, **kargs)
    fcntl.fcntl(self.stdout, fcntl.F_SETFL, os.O_NONBLOCK) 
    fcntl.fcntl(self.stderr, fcntl.F_SETFL, os.O_NONBLOCK)
