import unittest
from Movie import Movie
from Frame import Frame
from camera.camera import setupParser

TESTFILM_PATH = "/tmp/testFilm.flm"
class Test_Movie(unittest.TestCase):
  """ A set of test cases for movies. """

  def setUp(self):
    """ Setup: just construct a movie """
    self.movie = Movie()
  
   
  def test_AddFrame(self):
    """ Addition of a frame in order should yield correct IDs """
    frame1 = Frame(command = "command1", response = "response1")    
    self.assertTrue(frame1.is_processed())
    self.movie.addFrame(frame1)

    frame2 = Frame(command = "command2", response = "response2")    
    self.movie.addFrame(frame2)

    frame3 = Frame(command = "command3", response = "response3")    
    self.movie.addFrame(frame3)
    
    self.assertEquals(self.movie.getLength(), 3)
    self.assertEquals(frame1.getId(), 0)
    self.assertEquals(frame1.get_dependencies(), [])
    self.assertEquals(frame2.getId(), 1)
    self.assertEquals(frame2.get_dependencies(), [frame1])
    self.assertEquals(frame3.getId(), 2)
    self.assertEquals(frame3.get_dependencies(), [frame2])
  
  def test_set_response(self):
    """ Set frame response. """
    """ TODO: Put this in separate test case? """
    frame = Frame()
    self.assertFalse(frame.is_processed())
    frame.set_response("Passed")
    self.assertEquals("Passed", frame.getResponse())
    self.assertTrue(frame.is_processed())

  def _storeOpenAndCompareMovie(self):
    self.movie.toFile(TESTFILM_PATH)
    importMov = Movie()
    importMov.openFile(TESTFILM_PATH)
    
    self.assertEquals(str(self.movie.toxml()), str(importMov.toxml()))

  def testToFromXML(self):
    """ Writing and loading an empty Movie should give the same document """
    self._storeOpenAndCompareMovie()
      
  def testAddToFromXML(self):
    self.movie.addFrame(Frame(command="cmd", response="resp"))
    self._storeOpenAndCompareMovie()
  
  def testSemiEmptyExport(self):
    self.movie.addFrame(Frame(command="cmd", response=""))
    self._storeOpenAndCompareMovie()

  def testEmptyExport(self):
    self.movie.addFrame(Frame(command="cmd"))
    self._storeOpenAndCompareMovie()

  def testIds(self):
    """ Test if getFrameById works """
    f1 = Frame(command = "cmd1", response = "rsp1")
    f2 = Frame(command = "cmd2", response = "rsp2")
    self.movie.addFrame(f1)
    self.movie.addFrame(f2)
    
    f1ById = self.movie.getFrameById(f1.getId())

    self.assertEqual(f1, f1ById)
  
  def test_to_XML(self):
    """ Test toXML. """
    self.assertEquals(str(self.movie.toxml()).split()[0], "<?xml")
    self.assertEquals(1, str(self.movie.toxml()).count("DOCTYPE"))

  def test_title(self):
    """ Test set-get of title. """
    self.movie.set_title("Test")
    self.assertEquals("Test", self.movie.get_title())
                

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestMovie)
  unittest.TextTestRunner(verbosity=2).run(suite)

