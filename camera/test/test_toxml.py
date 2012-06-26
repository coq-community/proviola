import unittest
from lxml import etree
from Frame import Frame, TAG_ID, TAG_CMD, TAG_RES , TAG_DEPS 
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
        self.fail("Unexpected child: " + etree.tostring(child))

  def test_coqdoc_frame_toxml(self):
    """ Coqdoc frames. """
    from coqdoc_frame import Coqdoc_Frame, TAG_COQDOC
    from lxml import html
    element = Coqdoc_Frame(id = 42, command = "Foo", 
                           command_cd = [html.Element("b")],
                           response = "Bar").toxml_lxml()

    self.assertEquals("42", element.get(TAG_ID))

    self.assertEquals(4, len(list(element)))
    for child in element:
      if child.tag == TAG_CMD:
        self.assertEquals("Foo", child.text)
      elif child.tag == TAG_DEPS:
        self.assertEquals(0, len(child))
      elif child.tag == TAG_COQDOC:
        self.assertIn(html.Element("b").tag, [t.tag for t in list(child)])
      elif child.tag == TAG_RES:
        self.assertEquals("Bar", child.text)
      else:
        self.fail("Unexpected element: " + etree.tostring(child))

  def test_scenes_toxml(self):
    """ Scenes to XML. """
    from scene import Scene

    scene = Scene(no = 42)
    
    scene.add_scene(Scene(no = 481))
    scene.add_scene(Frame(id = 1337, command = "Foo"))
    
    xml = scene.toxml_lxml()
    self.assertEquals('42', xml.get("scenenumber"))
    
    self.assertEquals(2, len(list(xml)))
    for child in xml:
      if child.tag == 'scene':
        self.assertEquals('0', child.get("scenenumber"))
      elif child.tag == 'frame-reference':
        self.assertEquals('1337', child.get(TAG_ID))
      else:
        self.fail("Unexpected child: " + etree.tostring(child))


