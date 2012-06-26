# coding=utf-8
import unittest
from coq_local import Coq_Local
from mock import Mock, patch

_mock_select = Mock(return_value = ([], [], []))

class Test_Coq_Local(unittest.TestCase):
  """ Tests sending commands using a local installation for Coq. """
  
  def setUp(self):
    """ Setup local Coq session. """
    self._coq = Coq_Local(coqtop = "/usr/local/bin/coqtop")
    
  def test_send(self):
    """ Sending correct data to Coqtop should work. """
    self.assertIn("forall x : Type, x -> x",
      self._coq.send("Goal forall x, x->x."))
    self.assertEquals("", self._coq.send("Proof."))

  def test_send_utf8(self):
    """ Sending utf-8 should just work. """
    self._coq.send("Lemma foo : ∀ (x y z : nat), x + y + z = y + x + z.")
    
  def test_send_incorrect(self):
    """ Sending incorrect data should give an error report. """
    self.assertEquals(self._coq.send("Bogus."),
                      "Error: Unknown command of the non proof-editing mode.\n")
    
  def test_slow(self):
    """ Slow results should still be partitioned. """
    self._coq.send("Require Import Arith.")
    self._coq.send("Lemma loop x y : x + y = y + x.")
    self._coq.send("intros.")
    self._coq.send("Fail Timeout 2 repeat rewrite plus_comm.")
    self.assertFalse(self._coq.send("apply plus_comm.").startswith(
                                               "The command has indeed failed"),
                     "Started with output of previous command.") 
 
  def test_arguments(self):
    """ Passing arguments in the coqtop string should work. """
    Coq_Local(coqtop = '/usr/local/bin/coqtop -R /path ""')
