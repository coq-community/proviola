#!/usr/bin/env python
""" Convert Coqdoc HTML file into a documented movie, by sending the textual 
    contents of "code" divs to the camera.
"""
    
import argparse
import xml.parsers.expat
from xml.dom.minidom import parse

import coqdoc_parser

def create_arg_parser():
  """ Create an argument parser. """  
  parser = argparse.ArgumentParser(description = __doc__)
  parser.add_argument('coqdoc_file', type=argparse.FileType('r'))
  parser.add_argument('movie-file', type=argparse.FileType('w'), nargs="?")
  return parser

def convert_coqdoc(coqdoc_file): 
  """ Convert coqdoc_file into a movie, keeping the layout of coqdoc_file

    Arguments:
    - coqdoc_file: the source file, a valid file handler.
    
    Returns:
    - A movie containing the formatting of coqdoc_file, but with the code 
      augmented by the prover output.
  """
  p = coqdoc_parser.Coqdoc_Parser()
  p.feed(coqdoc_file.read())
  return p.get_coqdoc_movie()

if __name__ == '__main__':
  parser = create_arg_parser()
  args = parser.parse_args()
  narrated_movie = convert_coqdoc(args.coqdoc_file)
  narrated_movie.toxml()
#TODO: Write narrated_movie to args.movie-file
