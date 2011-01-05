import unittest
from BeautifulSoup import BeautifulStoneSoup

import sys
sys.path.append("../src")

import Reader
import Movie


class Test_CP(unittest.TestCase):
  """ Test cases for Coq using ProofWeb """
  
  def _normalize_xml(self, xml):
    """ Return a normalized XML file: one parsed by xml.dom.minidom and 
        pretty printed with spacing two (to increase readability in failed
        results.
    """
    return xml.prettify().strip()
  
  def setUp(self):
    """ Setup: create an empty movie for results """
    self.results = Movie.Movie()
    self.url = "http://hair-dryer.cs.ru.nl/proofweb/index.html"
    self.group = "nogroup"

  def test_empty_v(self):
    """ Empty file should return empty film. """

  
    expected_url = "exp/empty.flm"
    expected_xml = self._normalize_xml(BeautifulStoneSoup(open(expected_url, 'r').read()))
    
    data_url = "data/empty.v"
    reader = Reader.getReader(data_url)
    self.results = reader.make_frames(self.url, self.group)

    self.assertEquals(self._normalize_xml(self.results.toxml()), expected_xml)

  @classmethod
  def get_suite(cls):
    return unittest.TestLoader().loadTestsFromTestCase(cls)
