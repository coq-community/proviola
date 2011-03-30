from Reader import Reader, getReader
from CoqReader import CoqReader
from Isabelle_Reader import Isabelle_Reader
import unittest

class Test_Reader(unittest.TestCase):
  """ Test case for generic reader functionality. """
  
  def test_getReader_extension(self):
    """ Getting a reader by extension should provide the correct reader. """
    self.assertTrue(isinstance(getReader(extension = ".v"), 
                               CoqReader))
    self.assertTrue(isinstance(getReader(extension = ".thy"), 
                               Isabelle_Reader))
  def setUp(self):
    self.data = "Test data \n new line"
    self.reader = Reader()
    self.reader.add_code(self.data)
    
  def test_add_code(self):
    """ Test setting data. """
    
    self.assertEquals(self.data, self.reader.script)
    
  def test_reader_newline(self):
    """ Test that getting a new line yields the desired result. """
    self.assertEquals("Test data \n", self.reader.getLine())
    