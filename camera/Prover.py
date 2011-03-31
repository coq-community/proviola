class Prover(object):
  """ Fake prover implementation. """
  def send(self, command):
    return ""

from ProofWeb import ProofWeb
from coq_local import Coq_Local

def get_prover(url = None, group = None, path = None):
  """ Factory that determines what prover to serve. 
      For now, this is a wrapper around the ProofWeb constructor.
  """
  
  if path:
    return Coq_Local(path) 
  elif url and group:
    return ProofWeb(url, group)
  else:
    return Prover()