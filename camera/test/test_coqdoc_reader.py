# coding=utf-8
import unittest
from coqdoc_reader import Coqdoc_Reader

from mock import Mock
from Prover import get_prover

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
    self.assertEquals(result.get_scenes()[0].get_type(), "doc")
    self.assertEquals(result.getFrame(0).get_coqdoc_command(), 
                      "This is a non-code fragment.")
    self.assertFalse(result.getFrame(0).getResponse())
  
  def test_html_marked_doc(self):
    """ Marked up HTML should carry over. """
    self.reader.add_code(self.template.format(
                                      body = "<div><p>A paragraph</p></div>"))
    result = self.reader.make_frames(prover = self.mock_prover)
    
    self.assertEquals("<p>A paragraph</p>", 
                      str(result.getFrame(0).get_coqdoc_command()))
    
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
    
  
  def test_html_notation(self):  
    """ Test that Notation commands get extracted properly: there was a space
        missing somewhere. """
    self.reader.add_code(self.template.format(body =
       """<div class="code">
          <span>Notation </span><span>foo</span> := <span>nat</span>.</div>"""))
    
    result = self.reader.make_frames(prover = self.mock_prover)
    self.assertEquals("Notation foo := nat.", result.getFrame(0).getCommand())
  def test_html_two_dots(self):
    """ Two dots in the HTML should not be terminators. """
    self.reader.add_code(self.template.format(body = 
      '<div class="code"><span class="id" type="keyword">Notation</span> "[ x , .. , y ]" := (<a class="idref" href="Lists.html#NatList.cons"><span class="id" type="constructor">cons</span></a> <span class="id" type="var">x</span> .. (<a class="idref" href="Lists.html#NatList.cons"><span class="id" type="constructor">cons</span></a> <span class="id" type="var">y</span> <a class="idref" href="Lists.html#NatList.nil"><span class="id" type="constructor">nil</span></a>) ..).<br/></div>'))

    result = self.reader.make_frames(prover =  self.mock_prover)
    self.assertEquals(result.getFrame(0).getCommand(), 
      'Notation "[ x , .. , y ]" := (cons x .. (cons y nil) ..).')

  def test_html_single_code(self):
    """ Code divs should be picked up. """
    self.reader.add_code(self.template.format(body = 
                            """<div class="code">Code.</div>"""))
        
    result = self.reader.make_frames(prover = self.mock_prover)
    self.assertEquals(result.getFrame(0).getCommand(), "Code.")
    self.assertEquals(result.getFrame(0).get_coqdoc_command(), "Code.")
    self.assertEquals(result.getFrame(0).getResponse(), "Result")
  
  def test_html_marked_code(self):
    """ Code divs can (will) be marked up. """
    span = '<span class="id" type="keyword">Goal</span> <span class="id" type="keyword">forall</span> <span class="id" type="var">x</span>, <span class="id" type="var">x</span>-&gt;<span class="id" type="var">x</span>.' 
    markup = '<div class="code">' + span + '<br /></div>'
    self.reader.add_code(self.template.format(body = markup))
    
    result = self.reader.make_frames(prover = self.mock_prover)
    
    self.assertEquals(result.getFrame(0).getCommand(), "Goal forall x, x->x.")
    self.assertEquals(result.getFrame(0).getResponse(), "Result")
    self.assertEquals(str(result.getFrame(0).get_coqdoc_command()), span)
    self.assertEquals(str(result.getFrame(1).get_coqdoc_command()), "<br />")

  def test_html_marked_code_real(self):
    """ Extracted code should be readable by the PA. """
    markup = '<div class="code"><span class="id" type="keyword">Goal</span> <span class="id" type="keyword">forall</span> <span class="id" type="var">x</span>, <span class="id" type="var">x</span>-&gt;<span class="id" type="var">x</span>.</div>' 
    self.reader.add_code(self.template.format(body = markup))
    result = self.reader.make_frames(prover = get_prover())
    
    self.assertEquals(result.getFrame(0).getResponse(), """1 subgoal
  
  ============================
   forall x : Type, x -> x
""")
  
  def test_html_unicode(self):
    """ Unicode HTML should not give errors. """
    markup = '<div class="code">' +\
             'Lemma foo : ∀ (x y z : nat), x + y + z = y + x + z.</div>'
    self.reader.add_code(self.template.format(body = markup))
    self.reader.make_frames(prover = self.mock_prover)
        
        
  def test_title(self):
    """ Set a title if provided. """  
    self.reader.add_code("<html><head><title>Foo</title></head></html>")
    result = self.reader.make_frames(prover = self.mock_prover)
    self.assertEquals(result.get_title(), "Foo")
    
  def test_title_empty(self):
    """ Set an empty title if provided. """  
    self.reader.add_code("<html><head><title></title></head></html>")
    result = self.reader.make_frames(prover = self.mock_prover)
    self.assertEquals(result.get_title(), "")
  
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
  
  
