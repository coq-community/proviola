#! /usr/local/bin/python
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
import time
from Movie import Movie
import Reader
import os
import logging
from optparse import OptionParser
from argparse import ArgumentParser

def setupParser():
  """ Setup a command line parser """

  usage = """Usage: %prog [options] foo.v [bar.flm]
  Creates a movie from foo.v, storing in bar.flm, if provided, or in foo.flm."""

  parser = OptionParser(usage=usage)

  parser = ArgumentParser(description = usage)
  parser.add_argument("-u", "--user", 
                    action="store", dest="user",
                    default="nobody",
                    help="Username for ProofWeb (default: %default)")

  parser.add_argument("-g", "--group", 
                    action="store", dest="group",
                    default="nogroup",
                    help="Groupname for ProofWeb user (default: %default)")

  parser.add_argument("-p", "--password",
                    action="store", dest="pswd",
                    default="anon",
                    help="Password for user")
  parser.add_argument("--service_url",
                    action="store", dest="service",
                    default="http://hair-dryer.cs.ru.nl/proofweb/index.html",
                    help="""URL for web service to talk to prover
                          (default: %default)""")
  parser.add_argument("--prover",
                    action="store", dest="prover",
                    default="coq",
                    help="Prover to use (default: %default).")
  parser.add_argument("--stylesheet",
                    action="store", dest="stylesheet",
                    default="proviola.xsl",
                    help="URI at which the XSL stylesheet can be found (default: %default)")
  
  parser.add_argument("script", action="store", help="Script from which to make a movie")

  parser.add_argument("movie", action="store", nargs="?", default=None,
                      help="Movie file in which to store the constructed movie")
                    
  return parser

def main(argv = None):
  """ Main method: 
      - sets up logging information, 
      - parses the command line (optionally provided as a list),
      - creates a film out of the given script.
      - Writes the film to disk.

      Arguments:
      - Argv: Arguments passed to the options parser. 
  """

  logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

  parser = setupParser()
  options = parser.parse_args(argv)

  proofScript = options.script
  

  logging.debug("Processing: %s"%proofScript)

  movie = make_film(filename=proofScript, pwurl = options.service, group = options.group)

  if parser.movie:
    filmName = parser.movie
  else:
    filmName = Reader.getReader(proofScript).basename + ".flm" 

  directory = os.path.dirname(filmName)

  if len(directory) > 0 and not os.path.exists(directory):
    os.makedirs(directory)

  movie.toFile(filmName, options.stylesheet)

def make_film(filename, pwurl = None, group = "nogroup"):
  """Main method of the program/script: This creates a flattened 'film' for
   the given file filename.

    Arguments:
    - filename: The filename of the script to read.

    Keyword arguments:
    - pwurl: The URL to the server generating proof states.
    - group: The group used to log in.
  """ 

  reader = Reader.getReader(filename)
  try:
    return reader.make_frames(pwurl, group)
  except Exception as e:
    print "Exception: %s"%`e`
    return None


if __name__ == "__main__":
  sys.exit(main())
