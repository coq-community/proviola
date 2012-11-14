# coding=utf-8
import unittest
from tempfile import NamedTemporaryFile
from mock import MagicMock, Mock, patch 
from camera import camera

_mock_get_prover = Mock()
 
class TestCamera(unittest.TestCase):
  """ Test cases for the camera script and utilities. """
  
  def setUp(self):
    """ Create a parser. """
    self._parser = camera.setupParser()

  def test_parser_local(self):
    """ Test asking for a local Coq. """
    result = self._parser.parse_args(["--coqtop=foo", "--timeout=5", 
                                      "script.v"])
    self.assertEquals(result.coqtop, "foo")
    self.assertEquals(result.timeout, 5)
    
  def test_parser_short(self):
    """ Test that the command line parser is set up correctly. """
    self.assertTrue(self._parser.description)
    
    # Test short arguments 
    results_short = self._parser.parse_args(
        ["-ucarst",
         "-t5",
         "-gmathwiki",
         "-phackzor",
         "script.v"
        ])

    self.assertEquals(results_short.user,     "carst")
    self.assertEquals(results_short.timeout,  5)
    self.assertEquals(results_short.group,    "mathwiki")
    self.assertEquals(results_short.pswd,     "hackzor")
    self.assertEquals(results_short.script,   "script.v")
    self.assertFalse(results_short.movie)

  def test_parser_long(self):
    """ Test for long arguments. """
    #Test long arguments.
    results_long = self._parser.parse_args(
        ["--user=carst",
         "--group=mathwiki",
         "--password=hackzor",
         "--service-url=http://proofweb.cs.ru.nl",
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
  

  def test_parse_help(self):
    """ Test requesting help. """
    try:
      self._parser.parse_args(["-h"])
    except SystemExit as e:
      self.assertEquals(type(e), type(SystemExit()))
      self.assertEquals(e.code, 0)
    except e:
      self.fail("Unexpected exception %exp".format(exp=e))
    else:
      self.fail("SystemExit exception expected.")

  @patch('camera.camera.get_prover', _mock_get_prover)
  def test_user_specified_coqtop(self):
    """ Use the prover (Coqtop) specified in make_film. """
    f = NamedTemporaryFile(suffix = ".v")
    camera.make_film(f.name, coqtop = "/usr/bin/coqtop")
    f.close()
    
    self.assertTrue("/usr/bin/coqtop" in _mock_get_prover.call_args[1].values(),
                    "Specified path not used.")

  @patch('camera.camera.get_prover', _mock_get_prover)  
  def test_use_specified_proofweb(self):
    """ Use the prover (ProofWeb) specified in make_film. """
    f = NamedTemporaryFile(suffix = ".v")
    camera.make_film(f.name, 
                     pwurl = "http://prover.example.com")
    f.close()
    
    self.assertTrue("http://prover.example.com" in
                     _mock_get_prover.call_args[1].values(),
                    "Specified path not used.")
  
  @patch("camera.camera.get_prover", MagicMock())
  def test_unicode_file(self):
    """ A Unicode file should be 'converted' to a Unicode string."""
    with patch("camera.camera.get_reader", MagicMock()) as fake_reader:
      f = NamedTemporaryFile(suffix=".html")
      f.write(u"ζ".encode("utf-8"))
      f.flush()

      camera.make_film(f.name)
      fake_reader.return_value.add_code.assert_called_with(u"ζ")
      
      f.close()

      f = NamedTemporaryFile(suffix=".html")
      f.write("Foo")
      f.flush()
      camera.make_film(f.name)
      fake_reader.return_value.add_code.assert_called_with("Foo")
      f.close()


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCamera)
  unittest.TextTestRunner(verbosity=2).run(suite)

  
 
