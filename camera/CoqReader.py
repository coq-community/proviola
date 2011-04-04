""" A reader for Coq script files. 
    The parsing algorithm is rather naive: dot followed by whitespace 
    equals command. """

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

import string

from Reader import Reader
from Movie import Movie
from Frame import Frame

suffix = '.v'

class CoqReader(Reader):
  def __init__(self):
    Reader.__init__(self)
    self.unfinished = None

  def getComment(self, acc, open = 1):
    char = self.readChar() 
    while char != None and open > 0:
      acc = acc + char
      if char == "*":
        char2 = self.peekChar()
        if char2 == ")":
          acc = acc + self.readChar()
          open -= 1
          if open == 0:
            break
      elif char == "(":
        char2 = self.peekChar()
        if char2 == "*":
          acc = acc + self.readChar()
          open += 1
      char = self.readChar() 
    return acc

  def terminator(self, char, open):
    return  char == "." and self.peekChar() in string.whitespace and open == 0

  def getWord(self, acc, open = 0):
    char = self.readChar()
    while char != None:
      acc += char

      if self.terminator(char, open):
        break
      if char == "." and self.peekChar() == '.':
        acc += self.readChar()

      if char == "(":
        char2 = self.peekChar()
        if char2 == "*":
          acc = acc + self.readChar()
          open += 1
      elif char == "*":
        char2 = self.peekChar()
        if char2 == ")":
          acc = acc + self.readChar()
          open -= 1

      char = self.readChar()

    return acc
      
  def getCommand(self, acc = ""):
    
    char = self.readChar()
    while char != None:
      acc += char
      if char == "(":
        char2 = self.peekChar()
        if char2 == "*":
          acc = acc + self.readChar()
          return self.getComment(acc)
        else:
          return self.getWord(acc)

      elif not(char in string.whitespace): 
        return self.getWord(acc)
      char = self.readChar()
      
    return acc

  def parse(self, buffer):
    self.script += buffer
    if self.unfinished:
      acc = self.unfinished
    else:
      acc = ""
    
    command = self.getCommand(acc = acc)
    
    result = []
    while (len(command) != 0):
      if not (self.isCommand(command) or self.isComment(command)):
        self.unfinished = command
        command = ""
      else:
        self.unfinished = ""
        result.append(command)
        command = self.getCommand()
    
    if self.unfinished:
      result.append(self.unfinished)
      
    return result

  def isComment(self, text):
    """ Return whether the given text is a comment. """
    return len(text.split()) <= 0 or\
           text.split()[0].startswith("(*") and text.endswith("*)")
  
  def isCommand(self, text):
    """ Return whether the given text is a Coq comment. """
    text = text.rstrip()
    if text:
      return self.terminator(text.rstrip()[len(text) - 1], 0)
  
  def make_frames(self, prover = None):
    """ Splits the file stored in self.script into seperate commands, 
        and pairs these commands to their responses as provided by prover.

        Arguments:
        - prover: The prover to send commands to.
    """
    
    document = Movie()
    command = self.getCommand()
    
    while command != None and len(command) != 0:
      if self.isComment(command):
        response = None
      else:
        response = prover.send(command)
      
      id = 0
      document.addFrame(Frame(id, command, response))
      command = self.getCommand()

    return document

