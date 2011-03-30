import unittest 
from camera import camera

class TestCamera(unittest.TestCase):
  """ Test cases for the camera script and utilities. """

  def testParser(self):
    """ Test that the command line parser is set up correctly. """
    parser = camera.setupParser()
    
    self.assertTrue(parser.description)
    
    # Test short arguments 
    results_short = parser.parse_args(
        ["-ucarst", 
         "-gmathwiki",
         "-phackzor",
         "script.v"
        ])

    self.assertEquals(results_short.user,     "carst")
    self.assertEquals(results_short.group,    "mathwiki")
    self.assertEquals(results_short.pswd,     "hackzor")
    self.assertEquals(results_short.script,   "script.v")
    self.assertFalse(results_short.movie)

    #Test long arguments.
    results_long = parser.parse_args(
        ["--user=carst",
         "--group=mathwiki",
         "--password=hackzor",
         "--service_url=http://proofweb.cs.ru.nl",
         "--prover=isabelle",
         "--stylesheet=new.xsl", 
         "script.v",
         "movie.xml"])
    
    self.assertEquals(results_long.user,       "carst")
    self.assertEquals(results_long.group,      "mathwiki")
    self.assertEquals(results_long.pswd,       "hackzor")
    self.assertEquals(results_long.service,    "http://proofweb.cs.ru.nl")
    self.assertEquals(results_long.prover,     "isabelle")
    self.assertEquals(results_long.stylesheet, "new.xsl")
    self.assertEquals(results_long.movie, "movie.xml")
      
    # Requesting help should not fail
    try:
      parser.parse_args(["-h"])
    except SystemExit as e:
      self.assertEquals(type(e), type(SystemExit()))
      self.assertEquals(e.code, 0)
    except e:
      self.fail("Unexpected exception %exp".format(exp=e))
    else:
      self.fail("SystemExit exception expected.")


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCamera)
  unittest.TextTestRunner(verbosity=2).run(suite)
