import unittest
import CoqReader
import Reader

class Test_Reader(unittest.TestCase):
  """ Test for reader """

  def setUp(self):
    """ Setup creates a reader. """
    self.reader = CoqReader.CoqReader()

  def test_comment(self):
    """ Comments are also commands (for our purposes). """
    command = "(* A comment *) Goal forall x, x->x."
    actual = self.reader.parse(command)
    self.assertTrue(len(actual), 2)

  def test_parse_no_cmd(self):
   """ One unfinished command should produce a singleton list. """
   command = "Goa"
   expected = [command]
   actual = self.reader.parse(command)
   self.assertEquals(actual, expected)

  def test_parse_one(self):
    """ Test if the parser creates a singleton list for one command.  """
    command = "Goal forall x, x->x."
    expected = [command]
    actual = self.reader.parse(command)
    self.assertEquals(actual, expected)
  
  def test_parse_two(self):
    """ More than one command should create a list of more than one command. 
    """
    command = "Goal forall x, x->x. Proof. intros."
    actual = self.reader.parse(command)
    self.assertTrue(len(actual) == 3)
    
  def test_parse_continue(self):
    """ Adding new stuff to the parser should work. """
    command1 = "Goal forall x,\n"
    command2 = "x->x."
    
    actual = self.reader.parse(command1)
    
    self.assertEquals(actual, [command1])
    
    actual = self.reader.parse(command2)
    self.assertEquals(actual, [command1 + command2])

  def test_simple(self):
    """ Raw reader. """
    reader = Reader.Reader()
    reader.add_code("Frame1\nFrame2\n")
    movie = reader.make_frames()
    self.assertEquals(2, len(movie.get_frames()))
    self.assertEquals("Frame1\n", movie.get_frames()[0].getCommand())
    self.assertEquals("Frame2\n", movie.get_frames()[1].getCommand())

if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(Test_Reader)
  unittest.TextTestRunner(verbosity = 2).run(suite)
