import unittest
from xml.dom.minidom import parseString

import sys
sys.path.append("../src")

import Reader
import Movie

class Options_mock(object):
  """ Data class mockup for Options objects passed into Reader instances.
      TODO: For better testability (and portability, the options objects 
            should not be passed to deeper classes.
  """

  def __init__(self, url, group):
    self.pwurl = url
    self.group = group


class Test_CP(unittest.TestCase):
  """ Test cases for Coq using ProofWeb """
  
  def _normalize_xml(self, xml):
    """ Return a normalized XML file: one parsed by xml.dom.minidom and 
        pretty printed with spacing two (to increase readability in failed
        results.
    """
    return parseString(xml).toprettyxml(indent = "  ")
  
  def setUp(self):
    """ Setup: create an empty movie for results """
    self.results = Movie.Movie()
    self.options = Options_mock(
                 url = "http://hair-dryer.cs.ru.nl/proofweb/index.html",
                 group = "nogroup")

  def test_empty_v(self):
    """ Empty file should return empty film. """

  
    expected_url = "exp/empty.flm"
    expected_xml = self._normalize_xml(open(expected_url, 'r').read())

    data_url = "data/empty.v"
    reader = Reader.getReader(data_url)
    reader.make_frames(self.results, self.options)
    
    self.assertEquals(self._normalize_xml(self.results.toxml()), expected_xml)


  @classmethod
  def get_suite(cls):
    return unittest.TestLoader().loadTestsFromTestCase(cls)
