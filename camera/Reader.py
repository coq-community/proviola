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

class Reader:
  def __init__(self):
    """ Constructs an empty reader. """
    self.script = ""
    self.line = ""

  def getLine(self):
    """ Sets the line field to the next line in the script. 
        Returns the line. """
    if self.line == "":
      self.line = self.getNextLine()
      
    return self.line
  
  def getNextLine(self):  
    """ Get the next line in the script. """
    newLine = self.script.find("\n") if self.script else -1
    if newLine >= 0:
      result = self.script[0:newLine + 1]
      self.script =  self.script[newLine + 1 :]
      
    else:
      result = self.script
      self.script = "" 
    return result  
    
  def readChar(self):
    """ Read the next character in the script, updating the position. """
    line = self.getLine()
    if len(line) == 0:
      return None
    
    char = line[0]
    self.line = self.line[1:]
    return char
  
  def peekChar(self):
    """ Read the next character in the script, not updating the position. """
    line = self.getLine()
    if len(line) > 0:
      return line[0]
    else:
      return ' '
  
  def add_code(self, code):
    """ Add the given code to the managed script. """
    self.script += code

      
import CoqReader
import Isabelle_Reader
import os

def getReader(extension = None):
  # Setup dictionary of possible readers
  readers = {} # suffix -> (String -> Reader)
  readers[CoqReader.suffix] = CoqReader.CoqReader
  readers[Isabelle_Reader.suffix] = Isabelle_Reader.Isabelle_Reader
  
  return readers[extension]()


