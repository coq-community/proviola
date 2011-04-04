import CoqReader
import Isabelle_Reader
import coqdoc_reader
import os

def get_reader(extension = None):
  # Setup dictionary of possible readers
  readers = {} # suffix -> (String -> Reader)
  readers[CoqReader.suffix] = CoqReader.CoqReader
  readers[Isabelle_Reader.suffix] = Isabelle_Reader.Isabelle_Reader
  readers[coqdoc_reader.suffix] = coqdoc_reader.Coqdoc_Reader
  
  return readers[extension]()

