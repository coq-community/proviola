import unittest
from lxml import etree
from frame_factory import make_frame

from Frame import Frame
from coqdoc_frame import Coqdoc_Frame

class Test_Frame_Factory(unittest.TestCase):
  """ Test case exercising a factory of frames. """

  def _make_elem(self, contents):
    """ Build a frame element from the frame contents. """
    return etree.fromstring("""<film><frame framenumber="1">
      {contents}
      </frame></film>""".format(contents = contents)).find(".//frame")

  def test_simple_frame(self):
    """ A frame without a Coqdoc command should instantiate to a standard
        Frame.
    """
    element = self._make_elem("""<command>Test</command>
                                 <response>Response</response>
                                 <dependencies><dependency framenumber="0" /></dependencies>""")

    frame = make_frame(element)

    self.assertTrue(isinstance(frame, Frame))
    self.assertEquals("Test", frame.getCommand())
    self.assertEquals("Response", frame.getResponse())
    self.assertEquals([0], frame.get_dependencies())

  def test_coqdoc_frame(self):
    """ Frame containing a command-coqdoc section should yield a Coqdoc Frame. 
    """
    element = self._make_elem("""<command>Test</command>
      <command-coqdoc>Test-coqdoc</command-coqdoc>
      <response>Response</response>
      <dependencies><dependency framenumber="1" />
                    <dependency framenumber="2"/></dependencies>""")

    frame = make_frame(element)
    self.assertTrue(isinstance(frame, Coqdoc_Frame))
    self.assertEquals("Test", frame.getCommand())
    self.assertEquals("Test-coqdoc", frame.get_coqdoc_command())
    self.assertEquals("Response", frame.getResponse())
    self.assertEquals([1,2], frame.get_dependencies())
