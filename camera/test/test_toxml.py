import unittest
from Frame import Frame, TAG_CMD, TAG_RES , TAG_DEPS, TAG_ID
from lxml import etree

class test_toxml(unittest.TestCase):
  """ Testing various toxml methods. """

  def test_frame_toxml(self):
    """ Frames to XML. """
    frame_xml = Frame(id = 42,command = "Foo", response = "Bar").toxml_lxml()
    
    self.assertEquals("42", frame_xml.get(TAG_ID))
    for child in frame_xml:
      if child.tag == TAG_CMD:
        self.assertEquals("Foo", child.text)
      elif child.tag == TAG_RES:
        self.assertEquals("Bar", child.text)
      elif child.tag == TAG_DEPS:
        self.assertEquals([], list(child))
      else:
        self.fail("Unexpected child: ", etree.tostring(child))


