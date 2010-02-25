#! /usr/bin/python
import sys

from Film import FilmDocument
import Reader
from ProofWeb import ProofWeb

"""Main method
"""
def main(argv = None):
  if argv is None:
    argv = sys.argv
  if len(argv) > 1:
    proofScript = argv[1]
    print "Processing: %s"%proofScript
  else:
    print "Too few arguments"
    return 2
  
  sys.setrecursionlimit(2000)
  make_film(proofScript)

"""Main method of the program/script: This creates a flattened 'film' for
   the given file filename
"""
def make_film(filename):
  reader = Reader.getReader(filename)
  doc = FilmDocument()
  pw = ProofWeb("http://hair-dryer.cs.ru.nl/proofweb/index.html")
 
  basename = reader.basename
  reader.makeFrames(doc, pw)

  filmName = basename + ".flm" 
  doc.writeFilm(filmName)

if __name__ == "__main__":
  sys.exit(main())
