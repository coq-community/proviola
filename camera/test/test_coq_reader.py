import unittest
import CoqReader
from coq_local import Coq_Local
from mock import Mock

class Test_Coq_Reader(unittest.TestCase):
  """ Test cases for Coq using ProofWeb """
  def setUp(self):
    """ Setup fake prover. """
    self._prover = Mock()
    self._prover.send = Mock(return_value =  """1 subgoal
  
  ============================
   forall x : Type, x -> x
""")        
    self._reader = CoqReader.CoqReader()
    
  def test_empty_v(self):
    """ Empty data should return empty film. """
    self._reader.add_code("")
    result = self._reader.make_frames(prover = self._prover)
    self.assertEquals(result.getLength(), 0)
  
  def test_single(self):
    """ Single commands should return a goal. """
    self._reader.add_code("Goal forall x, x->x.")
    movie = self._reader.make_frames(prover = self._prover)
    self.assertEquals(movie.getLength(), 1)
    
    frame = movie.getFrame(0)
    self.assertEquals(frame.getCommand(),"Goal forall x, x->x.")
    self.assertEquals(frame.getResponse(), """1 subgoal
  
  ============================
   forall x : Type, x -> x
""")                    
  
  def test_slow(self):
    """ Test that a slow script gets processed correctly. """
    prover = Coq_Local("/usr/local/bin/coqtop")
    self._reader.add_code("""Require Import Arith.
Lemma loop x y : x + y = y + x.
intros.
Fail Timeout 2 repeat rewrite plus_comm.
apply plus_comm.
Qed. 
    """)
    movie = self._reader.make_frames(prover = prover)
    self.assertTrue(movie.getFrame(3).getResponse())

  @classmethod
  def get_suite(cls):
    return unittest.TestLoader().loadTestsFromTestCase(cls)
