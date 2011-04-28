import unittest
from mock import Mock, patch

from Prover import get_prover, Prover
from ProofWeb import ProofWeb
from coq_local import Coq_Local

_mock_which_none = Mock(return_value = None)
_mock_which_some = Mock(return_value = "/usr/bin/coqtop")

class Test_Prover(unittest.TestCase):
  """ TestCase exercising the prover module. """
  
  def test_factory(self):
    """ Test that the factory returns the appropriate PA. """
    self.assertTrue(isinstance(get_prover(path = "/usr/bin/coqtop"), Coq_Local))
    self.assertTrue(isinstance(
              get_prover(url = "http://prover.cs.ru.nl/index.html", 
                         group = "nogroup"), 
              ProofWeb))
    
  @patch("Prover.local_which", _mock_which_none)
  def test_factory_which_none(self):
    """ Tests that the factory returns a generic Prover instance if "which" 
        returns None.
    """
    self.assertTrue(isinstance(
                      get_prover(url = None, group = None, path = None),
                      Prover))

  @patch("Prover.local_which", _mock_which_some)
  def test_factory_which_some(self):
    """ If which returns a path, a Coq_Local instance using that path should be 
        created. 
    """
    self.assertTrue(isinstance(
                      get_prover(url = None, group = None, path = None),
                      Coq_Local))
