#!/usr/bin/env python
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


from Reader_Factory import get_reader

import sys
import os
from os.path import splitext
import logging
from argparse import ArgumentParser
from Prover import get_prover

def setupParser():
  """ Setup a command line parser """

  usage = """ Creates a movie from foo.v, storing in bar.flm, if provided,
              or in foo.flm."""


  parser = ArgumentParser(description = usage)
  parser.add_argument("-u", "--user", 
                    action="store", dest="user",
                    default="nobody",
                    help="Username for ProofWeb (default: %(default)s)")

  parser.add_argument("-g", "--group", 
                    action="store", dest="group",
                    default="nogroup",
                    help="Groupname for ProofWeb user (default: %(default)s)")

  parser.add_argument("-p", "--password",
                    action="store", dest="pswd",
                    default="anon",
                    help="Password for user")
  
  parser.add_argument("--coqtop", 
                      action = "store", dest = "coqtop",
                      default=None,
                      help = "Location of coqtop executable."
                      )
  
  parser.add_argument("--timeout", "-t",
                      action = "store", dest = "timeout",
                      type = float, default = 1,
                      help = """How long to wait for responses by coqtop. 
                      (In seconds, floating point).
                      """)
    
  parser.add_argument("--service-url",
                    action="store", dest="service",
                    default=None,
                    help="URL for web service to talk to prover")
  
  parser.add_argument("--prover",
                    action="store", dest="prover",
                    default="coq",
                    help="Prover to use (default: %(default)s).")
  
  parser.add_argument("--stylesheet",
                    action="store", dest="stylesheet",
                    default="proviola.xsl",
                    help="URI at which the XSL stylesheet can be found\
                      (default: %(default)s)")
  
  parser.add_argument("script", action="store", 
                      help="Script from which to make a movie")

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

  movie = make_film(filename=proofScript, 
                    coqtop = options.coqtop,
                    pwurl = options.service, 
                    group = options.group)

  if options.movie:
    filmName = options.movie
  else:
    filmName = splitext(proofScript)[0] + ".flm" 

  directory = os.path.dirname(filmName)

  if len(directory) > 0 and not os.path.exists(directory):
    os.makedirs(directory)
  
  movie.toFile(filmName, options.stylesheet)

def make_film(filename, pwurl = None, group = "nogroup",
                        coqtop = None):
  """Main method of the program/script: This creates a flattened 'film' for
   the given file filename.

    Arguments:
    - filename: The filename of the script to read.

    Keyword arguments:
    - pwurl: The URL to the server generating proof states.
    - group: The group used to log in.
  """ 

  extension = splitext(filename)[1] 
  reader = get_reader(extension = extension)
  reader.add_code(open(filename, 'r').read())
  
  
  prover = get_prover(path = coqtop, url = pwurl, group = group)

  return reader.make_frames(prover = prover)
  

if __name__ == "__main__":
  sys.exit(main())
