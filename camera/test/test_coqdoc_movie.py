import unittest
from tempfile import NamedTemporaryFile
from os import remove
from os.path import basename, dirname, join

from external.BeautifulSoup import BeautifulStoneSoup, Tag
from coqdoc_frame import Coqdoc_Frame

from coqdoc_movie import Coqdoc_Movie

class Test_Coqdoc_Movie(unittest.TestCase):
  """ Test several aspects of a Coqdoc movie. """
  
  def setUp(self):
    """ Sets up fixture. """
    self._target = NamedTemporaryFile(suffix = ".xml", delete = False)
    s = BeautifulStoneSoup()
    self._a = Tag(s, "a") 
    self._frame = Coqdoc_Frame(command_cd = [self._a], command = "foo", 
                               response = None)
    
    self._coqdoc_movie = Coqdoc_Movie()
    self._coqdoc_movie.addFrame(self._frame)

  
  def test_to_file_parents(self):
    """ When asked to write to a directory that does not yet exist, the 
        toFile function should create that directory. """
    filename = join(dirname(self._target.name), "new", 
                    basename(self._target.name))
    
    self._coqdoc_movie.toFile(filename)
    
  def test_from_string(self):
    """ Import a document from a string representation of the xml. """
    xml = """<?xml encoding="utf-8" version="1.0" ?>
             <?xml-stylesheet type="text/xsl" href="proviola.xsl" ?>
             <movie>
               <film>
                  <frame framenumber="0">
                    <command>Spam</command>
                    <response>Eggs</response>
                    <command-coqdoc><div>Spam</div></command-coqdoc>
                  </frame>
                </film>
                <scenes>
                  <scene id="page" scenenumber="0" class="doc">
                    <frame-reference framenumber="0" />
                  </scene>
                </scenes>  
              </movie>"""
              
    self._coqdoc_movie.from_string(xml)
    frame = self._coqdoc_movie.get_frames()[0]
    self.assertEquals(frame.getCommand(), "Spam")
    self.assertEquals(frame.getResponse(), "Eggs")
    self.assertEquals(str(frame.get_coqdoc_command()), "<div>Spam</div>")
    

  def test_title(self):
    """ Test set-get of title. """
    self._coqdoc_movie.set_title("Test")
    self.assertEquals("Test", self._coqdoc_movie.get_title())
                
    
  
