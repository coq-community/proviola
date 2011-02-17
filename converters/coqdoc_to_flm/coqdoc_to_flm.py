#!/usr/bin/env python
""" Convert Coqdoc HTML file into a documented movie, by sending the textual 
    contents of "code" divs to the camera.
"""
    
import argparse
from BeautifulSoup import BeautifulStoneSoup

from os.path import splitext, basename

import coqdoc_parser


def create_arg_parser():
  """ Create an argument parser. """  
  parser = argparse.ArgumentParser(description = __doc__)
  parser.add_argument('coqdoc_file', type=argparse.FileType('r'))
  parser.add_argument('movie_file', type=argparse.FileType('w'), nargs="?")
  return parser

def get_outfile(args):
  """ Get the outfile from the arguments. If it doesn't exist, it is the 
      infile with html substituted with xml.
      
      Returns:
        The outfile, opened for writing.
  """
  
  if args.movie_file:
    return args.movie_file
  else:
    return open(splitext(args.coqdoc_file.name)[0] + ".xml", 'w')

def replace_links(tree, from_link, to_link):
  """ Replace hyperlinks in the document of the name 'from_link' into 'to_link'
  
      Result
       tree  = tree[href="from_link" := href="to_link"]
  """
  for link in tree.findChildren(name = "a"):
    href = str(link.get("href"))
    if href.find(from_link) >= 0:
      link["href"] =  href.replace(from_link, to_link, 1)

def convert_coqdoc(coqdoc_data): 
  """ Convert coqdoc_file into a movie, keeping the layout of coqdoc_file

    Arguments:
    - coqdoc_file: the source file, a valid file handler.
    
    Returns:
    - A movie containing the formatting of coqdoc_file, but with the code 
      augmented by the prover output.
  """
  p = coqdoc_parser.Coqdoc_Parser()
  p.feed(coqdoc_data)
   
  return str(p.get_coqdoc_movie().toxml())

def create_movie(file, source, target):
  """ Create movie from the given HTML file, replacing links with links
      replaced to refer to the target file.
  """
  #Setup BeatifulStoneSoup to follow Wheaton's law.
  BeautifulStoneSoup.NESTABLE_TAGS["scene"] = []
  BeautifulStoneSoup.NESTABLE_TAGS["span"] = []

  narrated_movie = BeautifulStoneSoup(convert_coqdoc(file), 
                                      selfClosingTags = ["br"])
  replace_links(narrated_movie, source, target)
  return narrated_movie

if __name__ == '__main__':
  parser = create_arg_parser()
  args = parser.parse_args()
  print("File: {file}".format(file = args.coqdoc_file.name))
  # The selfClosingTags declaration is necessary to fix a nasty bug in which
  # a <br/> tag would eat the following tags.
  narrated_movie = create_movie(args.coqdoc_file.read(), 
                                basename(args.coqdoc_file.name),
                                basename(get_outfile(args).name))

#  narrated_movie = BeautifulStoneSoup(convert_coqdoc(args.coqdoc_file.read()),
#                                      selfClosingTags = ["br"])
#
#  replace_links(narrated_movie, basename(args.coqdoc_file.name), 
#                                basename(get_outfile(args).name))
  
  get_outfile(args).write(str(narrated_movie))
