from Reader_Factory import get_reader
from Reader import Reader
from CoqReader import CoqReader
from Isabelle_Reader import Isabelle_Reader
from coqdoc_reader import Coqdoc_Reader 
import unittest

class Test_Reader(unittest.TestCase):
  """ Test case for generic reader functionality. """
  
  def test_get_reader_extension(self):
    """ Getting a reader by extension should provide the correct reader. """
    self.assertTrue(isinstance(get_reader(extension = ".v"), 
                               CoqReader))
    self.assertTrue(isinstance(get_reader(extension = ".thy"), 
                               Isabelle_Reader))
    self.assertTrue(isinstance(get_reader(extension = ".html"), 
                               Coqdoc_Reader))
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
    
