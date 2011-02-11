import unittest
import re
import sys

sys.path.append("../../")
import coqdoc_parser
from BeautifulSoup import BeautifulSoup

class Coqdoc_Test(unittest.TestCase):
  
  def setUp(self):
    self._parser = coqdoc_parser.Coqdoc_Parser()
    
  def test_comment(self):
    """ Comments are exported properly. """
    
    # Preface.html (from the SF course notes) contains a "Version" comment. 
    file_contents = open("data/Preface.html", 'r').read()
    
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie().toxml()
    
    for child in movie.findAll(name = "span", recursive=True):
      if child.get("class") == "comment":
        return
    
    # Only reachable if we don't find a comment-span.
    self.assertTrue(False, "No comment in the processed code. ")
     
  def test_nested(self):
    """ Nested divs should produce nested scenes. """
    file_contents = open("data/nested/nested.html", 'r').read()
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie()
    
    self.assertEquals(movie.getLength(), 9)
    
  def test_attributes(self):
    """ Attributes should carry over. """
    file_contents = open("data/Preface.html", 'r').read()
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie().toxml()
    
    if movie.findAll(attrs={"id": "page"}):
      return
    self.fail("No id attribute")
  
  def test_entities(self):
    """ HTML entities should not produce an error. """
    file_contents = open("data/ents/ents.html", 'r').read()
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie()
    movie = movie.toxml()
    
    self.assertFalse(movie.findAll(text = re.compile(".*[Ee]rror.*")),
                     "Error while sending text with HTML  entities")
      
  def test_nested_html(self):
    """ HTML in doc should get copied correctly. """
    file_contents = open("data/nested/nested_html.html", 'r').read()
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie().toxml()
    if movie.findAll(name="h1"):
      return 
  
    self.fail("No h1 element")
    
  def test_multiple(self):
    """ Multiple commands on one line are parsed properly. 
    """
    commands = open("data/multiple/Basics.html", "r").read()
    self._parser.feed(commands)
    movie = self._parser.get_coqdoc_movie()
    
    self.assertEquals(movie.getLength(), 7) 
   
  def test_title(self):
    """ Test if title is set properly. """
    file_content = open("data/Preface.html", 'r').read()
    self._parser.feed(file_content)
    
    self.assertTrue("Preface" in self._parser.get_coqdoc_movie()._title)
  
  def test_empty_node(self):
    """ This test tests that empty nodes get processed properly. """
    div = BeautifulSoup("<div></div>")
    self._parser._process_div(div)

    
  @classmethod
  def get_suite(cls):
    return unittest.TestLoader().loadTestsFromTestCase(cls)
  

if __name__ == "__main__":
  suite = unittest.TestSuite()
  suite.addTests([Coqdoc_Test.get_suite()])
  unittest.TextTestRunner(verbosity=2).run(suite) 
