class Prover(object):
  """ Fake prover implementation. """
  def send(self, command):
    return ""

from ProofWeb import ProofWeb
from coq_local import Coq_Local
from external import which

def local_which(program):
  """ Implementation of "which" for Python. """
  try:
    return which.which(program)
  except which.WhichError:
    print "Which error"
    return None
  
def get_prover(url = None, group = None, 
               path = None):
  """ Factory that determines what prover to serve. 
  """
  if path:
    return Coq_Local(path) 
  elif (url and group):
    return ProofWeb(url, group)
  elif local_which("coqtop"):
    return Coq_Local(local_which("coqtop"))
  else:
    return Prover()