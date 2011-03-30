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
  def test_add_code(self):
    """ Test setting data. """
    data = "Test data"
    reader = Reader()
    reader.add_code(data)
    self.assertEquals(data, reader.script)
    
  def test_reader_newline(self):
    """ Test that getting a new line yields the desired result. """ 