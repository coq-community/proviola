import unittest
from coqdoc_reader import Coqdoc_Reader
from mock import Mock

class Test_Coqdoc_Reader(unittest.TestCase):
  """ Test cases exercising a Coqdoc reader. """
  
  def setUp(self):
    """ Setup: prover interface, Coqdoc_Reader instance. """
    self.reader = Coqdoc_Reader()
    
    self.mock_prover = Mock()
    self.mock_prover.send = Mock(return_value = "Result")
    self.template = "<html><body>{body}</body></html>"
    
  def test_add_code(self):
    """ Test that adding HTML code creates a tree. """
    self.reader.add_code(self.template.format(body = ""))
    self.assertTrue(self.reader._coqdoc_tree.html.body)
        
  def test_html_empty(self):
    """ Test that an empty HTML file leads to no frames, no scenes. """
    self.reader.add_code(self.template.format(body = ""))
    result = self.reader.make_frames(prover = self.mock_prover)
    
    self.assertEquals(len(result.get_scenes()), 0)
  
  def test_html_single_doc(self):
    """ An html file containing a doc-element should produce a frame without
        output. 
    """
    self.reader.add_code(self.template.format(body = """
                      <div>This is a non-code fragment.</div>"""))

    result = self.reader.make_frames(prover = self.mock_prover)
    
    self.assertEquals(len(result.get_scenes()), 1)
    self.assertEquals(len(result.get_frames()), 1)
    self.assertEquals(result.getFrame(0).get_coqdoc_command(), 
                      "This is a non-code fragment.")
    self.assertFalse(result.getFrame(0).getResponse())
  
  def test_html_nested_doc(self):
    """ HTML can contained divs nested in other divs. """
    self.reader.add_code(self.template.format(body = 
                            """<div>Outer <div>Nested</div>Trail</div>"""))
    result = self.reader.make_frames(prover = self.mock_prover)
    
    # Structure:
    self.assertEquals(len(result.get_scenes()), 1)
    self.assertEquals(len(result.get_scenes()[0].get_subscenes()), 3)
    
    # Content
    self.assertEquals(len(result.get_frames()), 3)
    self.assertEquals(result.getFrame(0).getCommand(), "Outer ")
    self.assertEquals(result.getFrame(1).getCommand(), "Nested")    
    self.assertEquals(result.getFrame(2).getCommand(), "Trail")
    
    
  
  def test_html_single_code(self):
    """ Code divs should be picked up. """
    self.reader.add_code(self.template.format(body = 
                            """<div class="code">Code.</div>"""))
        
    result = self.reader.make_frames(prover = self.mock_prover)
    self.assertEquals(result.getFrame(0).getCommand(), "Code.")
    self.assertEquals(result.getFrame(0).getResponse(), "Result")
    
  def test_attributes(self):
    """ A div should keep the attributes when converted to scenes. """
    self.reader.add_code(self.template.format(body = """
                            <div id="One" class="doc">Foo</div>"""))
    result = self.reader.make_frames(prover = self.mock_prover)
    
    attrs = result.get_scenes()[0].get_attributes()
    self.assertTrue("id" in attrs.keys())
    self.assertEquals("One", attrs["id"])
    
    self.assertTrue("class" in attrs.keys())
    self.assertEquals("doc", attrs["class"])