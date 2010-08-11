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

from Movie import Movie
import Reader
import os
from optparse import OptionParser

def setupParser():
  """ Setup a command line parser """
  usage = """Usage: %prog [options] foo.v [bar.flm]
  Creates a movie from foo.v, storing in bar.flm, if provided, or in foo.flm."""

  parser = OptionParser(usage=usage)
  parser.add_option("-u", "--user", 
                    action="store", dest="user",
                    default="nobody",
                    help="Username for ProofWeb (default: %default)")

  parser.add_option("-g", "--group", 
                    action="store", dest="group",
                    default="nogroup",
                    help="Groupname for ProofWeb user (default: %default)")

  parser.add_option("-p", "--password",
                    action="store", dest="pswd",
                    default="anon",
                    help="Password for user")
  parser.add_option("--proofweb",
                    action="store", dest="pwurl",
                    default="http://hair-dryer.cs.ru.nl/proofweb/index.html",
                    help="URL for a ProofWeb installation (default: %default).")
  parser.add_option("--prover",
                    action="store", dest="prover",
                    default="coq",
                    help="Prover to use (default: %default).")
  parser.add_option("--stylesheet",
                    action="store", dest="stylesheet",
                    default="proviola.xsl",
                    help="URI at which the XSL stylesheet can be found (default: %default)")
                    
  return parser

def main(argv = None):
  """Main method
  """

  if argv is None:
    argv = sys.argv
  
  parser = setupParser()
  (options, args) = parser.parse_args(argv)
  
  try:
    proofScript = args[1]
  except: 
    parser.print_help()
    return 0
  
  try:
    filmName = args[2]
  except:
    filmName = None

  print "Processing: %s"%proofScript

  make_film(proofScript, filmName, options=options)


def make_film(filename, filmName = None, stylesheet = "proviola.xsl",
              options = None):
  """Main method of the program/script: This creates a flattened 'film' for
   the given file filename
  """ 
  reader = Reader.getReader(filename)
  movie = Movie()

  if options is None:
    raise Exception("Options is none")
  else:
    stylesheet = options.stylesheet
  
  reader.makeFrames(movie, options)

  if filmName is None:
    basename = reader.basename
    filmName = basename + ".flm" 
  
  directory = os.path.dirname(filmName)
  
  if len(directory) > 0 and not os.path.exists(directory):
    os.makedirs(directory)
  
  movie.toFile(filmName, stylesheet)

if __name__ == "__main__":
  sys.exit(main())
