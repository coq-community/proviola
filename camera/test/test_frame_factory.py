import unittest
from external.BeautifulSoup import BeautifulStoneSoup
from frame_factory import make_frame
from Frame import Frame
from coqdoc_frame import Coqdoc_Frame

class Test_Frame_Factory(unittest.TestCase):
  """ Test case exercising a factory of frames. """

  def _make_elem(self, contents):
    """ Build a frame element from the frame contents. """
    return BeautifulStoneSoup("""<film><frame framenumber="1">
      {contents}
      </frame></film>""".format(contents = contents)).frame

  def test_simple_frame(self):
    """ A frame without a Coqdoc command should instantiate to a standard
        Frame.
    """
    element = self._make_elem("""<command>Test</command>
      <response>Response</response>""")

    frame = make_frame(element)

    self.assertTrue(isinstance(frame, Frame))
    self.assertEquals("Test", frame.getCommand())
    self.assertEquals("Response", frame.getResponse())

  def test_coqdoc_frame(self):
    """ Frame containing a command-coqdoc section should yield a Coqdoc Frame. 
    """
    element = self._make_elem("""<command>Test</command>
      <command-coqdoc>Test-coqdoc</command-coqdoc>
      <response>Response</response>""")

    frame = make_frame(element)
    self.assertTrue(isinstance(frame, Coqdoc_Frame))
    self.assertEquals("Test", frame.getCommand())
    self.assertEquals("Test-coqdoc", frame.get_coqdoc_command())
    self.assertEquals("Response", frame.getResponse())
