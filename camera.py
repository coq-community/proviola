#! /usr/bin/python
#
# Author: Carst Tankink carst 'at' cs 'dot' ru 'dot' nl
# Copyright: Radboud University Nijmegen
#
# This file is part of the Proof Camera.
#
# Proof Camera is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Proof Camera is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Proof Camera.  If not, see <http://www.gnu.org/licenses/>.


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
