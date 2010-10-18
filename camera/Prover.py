""" Base class for communicating with a prover.
"""

class Prover(object):
  """ Prover base class. """


from ProofWeb import ProofWeb
def get_prover(url, group):
  """ Factory that determines what prover to serve. 
      For now, this is a wrapper around the ProofWeb constructor.
  """
  return ProofWeb(url, group)
