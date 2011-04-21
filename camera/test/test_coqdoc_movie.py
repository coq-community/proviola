import unittest
from tempfile import NamedTemporaryFile
from os import remove
from external.BeautifulSoup import BeautifulStoneSoup, Tag
from coqdoc_frame import Coqdoc_Frame

from coqdoc_movie import Coqdoc_Movie

class Test_Coqdoc_Movie(unittest.TestCase):
  """ Test several aspects of a Coqdoc movie. """
  
  def setUp(self):
    """ Sets up fixture. """
    self._target = NamedTemporaryFile(suffix = ".xml", delete = False)
    s = BeautifulStoneSoup()
    self._a = Tag(s, "a") 
    self._frame = Coqdoc_Frame(command_cd = [self._a], command = "foo", 
                               response = None)
    
    self._coqdoc_movie = Coqdoc_Movie()
    self._coqdoc_movie.addFrame(self._frame)

  def test_html_links_internal(self):
    """ Internal links in the input should be replaced by links to the current 
        document. """    
    self._a["href"] = "test.html"
    self._a.append("link")
    
    self._coqdoc_movie.toFile(self._target.name)
    
    doc = BeautifulStoneSoup(self._target.read())
    new_a = doc.findAll(name = "a")[0]
    self.assertTrue(new_a.get("href").endswith(".xml"))
    remove(self._target.name)

  def test_html_links_external(self):
    """ Links to external files should not be renamed. """
    self._a["href"] = "http://example.com"
    self._a.append("link")
    
    self._coqdoc_movie.toFile(self._target.name)
    doc = BeautifulStoneSoup(self._target.read())
    new_a = doc.findAll(name = "a")[0] 
    self.assertEquals("http://example.com", new_a.get("href"))
  
  def test_html_links_anchor(self):
    """ Only the link before the anchor should be replaced. """
    self._a["href"] = "test.html#foo"
    self._a.append("link")
    
    self._coqdoc_movie.toFile(self._target.name)
    
    doc = BeautifulStoneSoup(self._target.read())
    new_a = doc.findAll(name = "a")[0]
    self.assertTrue(new_a.get("href").endswith(".xml#foo"))
    remove(self._target.name)   
