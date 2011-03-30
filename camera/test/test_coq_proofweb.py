import unittest
from BeautifulSoup import BeautifulStoneSoup
from os.path import join, dirname, abspath

import Reader

#TODO: This does not exercise the ProofWeb code, but the reader.

class Test_Coq_Proofweb(unittest.TestCase):
  """ Test cases for Coq using ProofWeb """
  
  def _normalize_xml(self, xml):
    """ Return a normalized XML file: one parsed by xml.dom.minidom and 
        pretty printed with spacing two (to increase readability in failed
        results.
    """
    return xml.prettify().strip()
  
  def setUp(self):
    """ Setup Proofweb settings. """
    self.pw_url = "http://hair-dryer.cs.ru.nl/proofweb/index.html"
    self.group = "nogroup"
    self.reader = Reader.getReader(extension = ".v")
    
  def test_empty_v(self):
    """ Empty file should return empty film. """
    self.reader.add_code("")
    result = self.reader.make_frames(self.pw_url, self.group)
    self.assertEquals(result.getLength(), 0)
  
  def test_single(self):
    """ Single commands should return a goal. """
    self.reader.add_code("Goal forall x, x->x.")
    movie = self.reader.make_frames(self.pw_url, self.group)
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
