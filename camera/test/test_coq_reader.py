import unittest
import CoqReader
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
    
  @classmethod
  def get_suite(cls):
    return unittest.TestLoader().loadTestsFromTestCase(cls)
