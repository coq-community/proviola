import unittest

from Prover import get_prover, Prover
from ProofWeb import ProofWeb
from coq_local import Coq_Local

class Test_Prover(unittest.TestCase):
  """ TestCase exercising the prover module. """
  
  def test_factory(self):
    """ Test that the factory returns the appropriate PA. """
    self.assertTrue(isinstance(get_prover(path = "/usr/bin/coqtop"), Coq_Local))
    self.assertTrue(isinstance(
              get_prover(url = "http://hair-dryer.cs.ru.nl/proofweb/index.html", 
                         group = "nogroup"), 
              ProofWeb))
    self.assertTrue(isinstance(get_prover(), Prover))