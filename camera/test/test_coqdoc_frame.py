import unittest 
from external.BeautifulSoup import BeautifulStoneSoup
from coqdoc_frame import Coqdoc_Frame

class Test_Coqdoc_Frame(unittest.TestCase):
  """ Tests of the coqdoc frame. """
  

  def test_none(self):
    """ Frames with empty (None) commands/responses should still export. """
    frame = Coqdoc_Frame(command = None, command_cd = None, response = None)
    xml = frame.toxml(doc = BeautifulStoneSoup())
    self.assertEquals(xml.command.text, "")
    self.assertFalse(xml.response)
    self.assertFalse(xml.find(name = "command-coqdoc").text)

  def test_entitities(self):
    """ Test that entities in command, response and coqdoc_command are
        exported to the correct entitity codes when exporting to XML. """
    
    frame = Coqdoc_Frame(command = "&",
                         command_cd = "&", 
                         response = "&")
    
    xml = frame.toxml(doc = BeautifulStoneSoup())
    self.assertEquals(xml.command.text, "&amp;")
    print "XML (test): ", xml
    self.assertEquals(xml.response.text, "&amp;")
  
  def test_export_entities(self):
    """ Entities that are already escaped should not be escaped again. """
    frame = Coqdoc_Frame(command =" ", 
                         command_cd = BeautifulStoneSoup("<div>&nbsp;</div>"))
    xml = frame.toxml(doc = BeautifulStoneSoup())

    self.assertEquals(xml.find(name = "command-coqdoc").div.text, 
                      "&nbsp;")
  
  def test_from_xml(self):
    """ Test that a frame is constructed from XML, properly. """
    xml = BeautifulStoneSoup("""<film><frame framenumber="0">
      <command>Spam</command>
      <response>Eggs</response>
      <command-coqdoc><div>Spam</div></command-coqdoc>
    </frame></fiml>
     """)
    frame = Coqdoc_Frame()
    frame.fromxml(xml.frame)
    
    self.assertEquals("Spam", frame.getCommand())
    self.assertEquals("Eggs", frame.getResponse())
    self.assertEquals("<div>Spam</div>", str(frame.get_coqdoc_command()))
    self.assertEquals("<div>Spam</div>", str(frame.get_markup_command()))
    
  def test_nested_entities(self):
    """ Test that entities in elements escape correctly. """
    soup = BeautifulStoneSoup("<div>&amp;</div>")
    frame = Coqdoc_Frame(command = "foo", response = "bar",
                         command_cd = soup)
    
    xml = frame.toxml(doc = BeautifulStoneSoup())
    self.assertEquals(str(xml.find(name = "command-coqdoc").div), 
                      "<div>&amp;</div>")
