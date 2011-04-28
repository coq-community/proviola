import unittest 
from external.BeautifulSoup import BeautifulStoneSoup
from coqdoc_frame import Coqdoc_Frame

class Test_Coqdoc_Frame(unittest.TestCase):
  """ Tests of the coqdoc frame. """
  
  def test_entitities(self):
    """ Test that entities in command, response and coqdoc_command are
        exported to the correct entitity codes when exporting to XML. """
    
    frame = Coqdoc_Frame(command = "&",
                         command_cd = "&", 
                         response = "&")
    
    xml = frame.toxml(doc = BeautifulStoneSoup())
    self.assertEquals(xml.command.text, "&amp;")
    self.assertEquals(xml.response.text, "&amp;")
    self.assertEquals(xml.find(name = "command-coqdoc").text, "&amp;")
  
  def test_nested_entities(self):
    """ Test that nested entities work correctly. """
    soup = BeautifulStoneSoup("<div>&</div>")
    frame = Coqdoc_Frame(command = "foo", response = "bar",
                         command_cd = soup)
    
    xml = frame.toxml(doc = BeautifulStoneSoup())
    self.assertEquals(str(xml.find(name = "command-coqdoc").div), 
                      "<div>&amp;</div>")