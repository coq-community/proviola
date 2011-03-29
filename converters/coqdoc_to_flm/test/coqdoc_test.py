import unittest
import re
import sys
from os.path import join, dirname, abspath

sys.path.append("../../")
import coqdoc_parser
import coqdoc_to_flm
from coqdoc_movie import Coqdoc_Movie

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

class Coqdoc_Test(unittest.TestCase):

  def normalize(self, path):
    """ Normalize the path to the absolute path of the directory of __file__ """
    return join(dirname(abspath(__file__)), path)


  def setUp(self):
    self._parser = coqdoc_parser.Coqdoc_Parser()
    
  def test_comment(self):
    """ Comments are exported properly. """
    
    # Preface.html (from the SF course notes) contains a "Version" comment. 
    file_contents = open(self.normalize("data/Preface.html"), 'r').read()
    
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie().toxml()
    
    for child in movie.findAll(name = "span", recursive=True):
      if child.get("class") == "comment":
        return
    
    # Only reachable if we don't find a comment-span.
    self.assertTrue(False, "No comment in the processed code. ")
     
  def test_nested(self):
    """ Nested divs should produce nested scenes. """
    file_contents = open(self.normalize("data/nested/nested.html"), 'r').read()
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie()
    
    self.assertEquals(movie.getLength(), 9)
    
  def test_attributes(self):
    """ Attributes should carry over. """
    file_contents = open(self.normalize("data/Preface.html"), 'r').read()
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie().toxml()
    
    if movie.findAll(attrs={"id": "page"}):
      return
    self.fail("No id attribute")
  
  def test_entities(self):
    """ HTML entities should not produce an error. """
    file_contents = open(self.normalize("data/ents/ents.html"), 'r').read()
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie()
    movie = movie.toxml()
    
    self.assertFalse(movie.findAll(text = re.compile(".*[Ee]rror.*")),
                     "Error while sending text with HTML  entities")
      
  def test_nested_html(self):
    """ HTML in doc should get copied correctly. """
    file_contents = open(self.normalize("data/nested/nested_html.html"), 
                         'r').read()
    self._parser.feed(file_contents)
    movie = self._parser.get_coqdoc_movie().toxml()
    if movie.findAll(name="h1"):
      return 
  
    self.fail("No h1 element")

  def test_no_title(self):
    """ Test resilience for empty title. """
    html = """
      <html>
        <head>
          <title></title>
        </head>
        <body/>
      </html>"""
    try:
      self._parser.feed(html)
      self._parser.get_coqdoc_movie().toxml()
    except TypeError as ex:
      self.fail("Error thrown when parsing an empty title.\n{error}".format(
                error=ex))



  def test_lt(self):
    """ The < character in code should be escaped to &lt; """
    data = """<html><head><title>foo</title></head>
              <body><div class="code">Goal forall x, x &lt;= x.</div>
              </body>"""
    self._parser.feed(data)
    movie = self._parser.get_coqdoc_movie().toxml()
    self.assertTrue("<" not in movie.film.text)

  def test_multiple(self):
    """ Multiple commands on one line are parsed properly. 
    """
    commands = open(self.normalize("data/multiple/Basics.html"), "r").read()
    self._parser.feed(commands)
    movie = self._parser.get_coqdoc_movie()
    
    self.assertEquals(movie.getLength(), 7) 
   
  def test_title(self):
    """ Test if title is set properly. """
    file_content = open(self.normalize("data/Preface.html"), 'r').read()
    self._parser.feed(file_content)
    
    self.assertTrue("Preface" in self._parser.get_coqdoc_movie()._title)
  
  def test_empty_node(self):
    """ Test that empty nodes get processed properly, without exceptions. """
    div = BeautifulSoup("<div></div>")
    self._parser._process_div(div)
  

  def test_nested_elems(self):
    """ Nested spans, scenes should get carried over properly. """
    spans = """<html><head><title>Spam</title></head>
              <body>
              <div>
                <div>
                  <span class="inlinecode">
                   <span class="id" type="var">
                    Spam
                   </span>
                   (
                   <span class="id" type="var">
                    Eggs
                   </span>
                   )
                  </span>
                </div>
              </div>
            </body></html>"""
    movie = coqdoc_to_flm.create_movie(spans, "ni", "formerly ni")

    # Scenes (= translated divs) should nest, so there should be one scene at
    # the top level.
    self.assertEquals(len(movie.scenes.findAll(recursive = False)), 1)

    # The first span (in the third frame in the film) should have a child span.
    self.assertTrue(movie.film.contents[2].span.span)
   
  def test_to_from_xml(self):
    """ Exporting making a roundtrip through xml should produce the same XML
        tree. """

    spans = """<html><head><title>Spam</title></head>
              <body>
              <div>
                <div>
                  <span class="inlinecode">
                   <span class="id" type="var">
                    Spam
                   </span>
                   (
                   <span class="id" type="var">
                    Eggs
                   </span>
                   )
                  </span>
                </div>
              </div>
            </body></html>"""

    movie = coqdoc_to_flm.create_movie(spans, "ni", "formerly ni")
    new_movie = Coqdoc_Movie()
    new_movie.fromxml(movie)

    self.assertEquals(str(movie), str(new_movie.toxml()))

  def test_from_xml_nested(self):
    """ From xml should respect nested scenes/frame references. """
    BeautifulStoneSoup.NESTABLE_TAGS["scene"] = []
    tree = BeautifulStoneSoup(
              """<movie>
                  <film>
                    <frame framenumber="0">
                      <command>Blah</command>
                      <command-coqdoc>Blah</command-coqdoc>
                      <response> Gamma |- Goal</response>
                    </frame>
                    <frame framenumber="1">
                      <command>Blah2</command>
                      <command-coqdoc>Blah2</command-coqdoc>
                      <response> Gamma2 |- Goal2</response>
                    </frame>
                  </film>
                  <scenes>
                    <scene scenenumber="1" class="test">
                      <scene scenenumber="2" class="test">
                        <frame-reference framenumber="0"/>
                      </scene>
                      <frame-reference framenumber="1"/>
                      <scene scenenumber="3" class="test">
                      </scene>
                    </scene>
                  </scenes>
                </movie>""")

    movie = Coqdoc_Movie()
    movie.fromxml(tree)
    for scene in movie.get_scenes():
      for sub in scene.get_subscenes():
        if sub.is_scene():
          for grandchild in sub.get_subscenes():
            self.assertTrue(grandchild.getCommand())
            self.assertTrue(grandchild.get_coqdoc_command())
            self.assertTrue(grandchild.getResponse())
        else:
          self.assertTrue(sub.getCommand())
          self.assertTrue(sub.get_coqdoc_command())
          self.assertTrue(sub.getResponse())



  @classmethod
  def get_suite(cls):
    return unittest.TestLoader().loadTestsFromTestCase(cls)
  

if __name__ == "__main__":
  suite = unittest.TestSuite()
  suite.addTests([Coqdoc_Test.get_suite()])
  unittest.TextTestRunner(verbosity=2).run(suite) 