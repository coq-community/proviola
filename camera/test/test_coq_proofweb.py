import unittest
from BeautifulSoup import BeautifulStoneSoup
from os.path import join, dirname, abspath
from StringIO import StringIO
import Reader


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
    self.dir = dirname(abspath(__file__))
    
  def test_empty_v(self):
    """ Empty file should return empty film. """
    data_url = join(self.dir, "data/empty.v")
    reader = Reader.getReader(data_url)
    result = reader.make_frames(self.pw_url, self.group)
    self.assertEquals(result.getLength(), 0)
  
  def test_single(self):
    """ Single commands should return a goal. """
    data_url = join(self.dir, "data/single.v")
    reader = Reader.getReader(data_url)
    movie = reader.make_frames(self.pw_url, self.group)
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