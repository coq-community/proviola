import unittest 
from coqdoc_frame import Coqdoc_Frame

from lxml import etree, html

class Test_Coqdoc_Frame(unittest.TestCase):
  """ Tests of the coqdoc frame. """
  
  def test_none(self):
    """ Frames with empty (None) commands/responses should still export. """
    frame = Coqdoc_Frame(command = None, command_cd = None, response = None)
    xml = frame.toxml()
    self.assertEquals([], list(xml.find(".//command")))
    self.assertEquals([], list(xml.find(".//response")))
    self.assertEquals([], list(xml.find(".//command-coqdoc")))

  def test_entitities(self):
    """ Test that entities in command, response and coqdoc_command are
        exported to the correct entitity codes when exporting to XML. """
    
    frame = Coqdoc_Frame(command = "&",
                         command_cd = "&", 
                         response = "&")
    
    xml = frame.toxml()
    self.assertEquals(xml.find(".//command").text, "&amp;")
    self.assertEquals(xml.find(".//response").text, "&amp;")
  
  def test_export_entities(self):
    """ Entities that are already escaped should not be escaped again. """
    frame = Coqdoc_Frame(command =" ", 
                         command_cd = [html.fromstring("<div>&nbsp;</div>")])
    xml = frame.toxml()

    self.assertEquals(xml.find(".//command-coqdoc")[0].text, 
                      u"\xa0")
  
  def test_from_xml(self):
    """ Test that a frame is constructed from XML, properly. """
    xml = etree.fromstring("""<frame framenumber="0">
      <command>Spam</command>
      <response>Eggs</response>
      <command-coqdoc><div>Spam</div></command-coqdoc>
      <dependencies />
    </frame>""")
    frame = Coqdoc_Frame()
    frame.fromxml(xml)
    
    self.assertEquals("Spam", frame.getCommand())
    self.assertEquals("Eggs", frame.getResponse())
    self.assertEquals("<div>Spam</div>", str(frame.get_coqdoc_command()))
    self.assertEquals("<div>Spam</div>", str(frame.get_markup_command()))
    self.assertFalse(frame.is_code())
    self.assertEquals([], frame.get_dependencies())

  def test_fromxml_code(self):
    """ Frames with an is_code attribute should have this set to True in the
        instantiated class.  """
    xml = etree.fromstring("""<frame framenumber="0" is_code="true">
                           <command>foo</command><command-coqdoc/></frame>""")
    frame = Coqdoc_Frame()
    frame.fromxml(xml)
    self.assertTrue(frame.is_code())


  def test_nested_entities(self):
    """ Test that entities in elements escape correctly. """
    soup = etree.fromstring("<div>&amp;</div>")
    frame = Coqdoc_Frame(command = "foo", response = "bar",
                         command_cd = [soup])
    
    xml = frame.toxml()
    self.assertEquals(etree.tostring(xml.find(".//command-coqdoc")[0]), 
                      "<div>&amp;</div>")
