import unittest
from Movie import Movie
from Frame import Frame
from scene import Scene
from camera.camera import setupParser

TESTFILM_PATH = "/tmp/testFilm.flm"
class Test_Movie(unittest.TestCase):
  """ A set of test cases for movies. """

  def setUp(self):
    """ Setup: just construct a movie """
    self.movie = Movie()
  
  def test_AddFrame(self):
    """ Addition of a frame. """
    s = Scene()
    self.movie.add_scene(s)

    frame1 = Frame(command = "command1", response = "response1")
    frame1.set_code(True)
    self.assertTrue(frame1.is_processed())

    s.add_scene(frame1)

    frame2 = Frame(command = "command2", response = "response2")    
    frame2.set_code(True)
    frame2.set_dependencies([frame1])

    s.add_scene(frame2)


    frame3 = Frame(command = "command3", response = "response3")    
    frame3.set_code(True)
    frame3.set_dependencies([frame2])
    s.add_scene(frame3)
    
    self.assertEquals(self.movie.getLength(), 3)
    self.assertEquals(frame1.get_dependencies(), [])
    self.assertEquals(frame2.get_dependencies(), [frame1])
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
    
    self.assertEquals(str(self.movie), str(importMov))

  def testToFromXML(self):
    """ Writing and loading an empty Movie should give the same document """
    self._storeOpenAndCompareMovie()
      
  def testAddToFromXML(self):
    scene = Scene()
    scene.add_scene(Frame(command="cmd", response="resp"))
    self.movie.add_scene(scene)
    self._storeOpenAndCompareMovie()
  
  def testSemiEmptyExport(self):
    s = Scene()
    s.add_scene(Frame(command="cmd", response=""))
    self.movie.add_scene(s)
    self._storeOpenAndCompareMovie()

  def testEmptyExport(self):
    scene = Scene()
    scene.add_scene(Frame(command="cmd"))
    self.movie.add_scene(scene)
    self._storeOpenAndCompareMovie()

  def testIds(self):
    """ Test if getFrameById works """
    s = Scene()
    f1 = Frame(command = "cmd1", response = "rsp1")
    f2 = Frame(command = "cmd2", response = "rsp2")
    s.add_scene(f1)
    s.add_scene(f2)
    self.movie.add_scene(s)
    
    f1ById = self.movie.getFrameById(f1.getId())

    self.assertEqual(f1, f1ById)

    self.assertIsNone(self.movie.getFrameById(42), "Id out of range")
  
  def test_to_XML(self):
    """ Going to string should give well-formed XML, with a stylesheet
        reference. """
    self.assertEquals(str(self.movie).split()[0], "<?xml")
    self.assertEquals(1, str(self.movie).count("xml-stylesheet"))
    self.assertEquals(1, str(self.movie).count("DOCTYPE"))
  
  def test_title(self):
    """ Test set-get of title. """
    self.movie.set_title("Test")
    self.assertEquals("Test", self.movie.get_title())
                

if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestMovie)
  unittest.TextTestRunner(verbosity=2).run(suite)

