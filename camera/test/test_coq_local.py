import unittest
from coq_local import Coq_Local
from mock import Mock, patch

_mock_select = Mock(return_value = ([], [], []))

class Test_Coq_Local(unittest.TestCase):
  """ Tests sending commands using a local installation for Coq. """
  
  def setUp(self):
    """ Setup local Coq session. """
    self._coq = Coq_Local(coqtop = "/usr/bin/coqtop", timeout = 2)
    
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
  
  @patch("select.select", _mock_select)
  def test_timeout(self):
    """ Test that a specified timeout is used. """
    Coq_Local(timeout = 10)
    self.assertTrue(10 in _mock_select.call_args[0])
    

  @patch("select.select", _mock_select)
  def test_timeout_send(self):
    """ Test that send uses specified timeout. """
    self._coq.send("Goal forall x, x->x.")
    self.assertTrue(2 in _mock_select.call_args[0])
    
    