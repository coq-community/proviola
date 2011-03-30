import unittest
from ProofWeb import ProofWeb
class Test_ProofWeb(unittest.TestCase):
  """ Test case exercising the ProofWeb protocol. """
  
  def setUp(self):
    self.proofweb = ProofWeb(
                        url = "http://hair-dryer.cs.ru.nl/proofweb/index.html",
                        group = "nogroup", user = "nobody", 
                        pswd = "anon", prover = "coq")
    
  def test_send(self):
    """ Sending correct data to Proofweb should work. """
    self.assertEquals(self.proofweb.send("Goal forall x, x->x."),
                      """1 subgoal
  
  ============================
   forall x : Type, x -> x
""")
  
  def test_send_incorrect(self):
    """ Sending incorrect data should give a ProofWeb errror report. """
    self.assertEquals(self.proofweb.send("Bogus."),
                      "Error: Unknown command of the non proof-editing mode.\n")