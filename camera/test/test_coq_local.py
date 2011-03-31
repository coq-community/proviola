import unittest
from coq_local import Coq_Local

class Test_Coq_Local(unittest.TestCase):
  """ Tests sending commands using a local installation for Coq. """
  
  def setUp(self):
    """ Setup local Coq session. """
    self._coq = Coq_Local("/usr/bin/coqtop")
    
  def test_send(self):
    """ Sending correct data to Coqtop should work. """
    self.assertEquals(self._coq.send("Goal forall x, x->x."),
                      """1 subgoal
  
  ============================
   forall x : Type, x -> x
""")
  
  def test_send_incorrect(self):
    """ Sending incorrect data should give an error report. """
    self.assertEquals(self._coq.send("Bogus."),
                      "Error: Unknown command of the non proof-editing mode.\n")