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
from coqdoc_frame import Coqdoc_Frame
from scene import Scene
from xml.sax.saxutils import escape

suffix = '.v'

class CoqReader(Reader):
  def __init__(self):
    Reader.__init__(self)
    self._deps = []
    self.unfinished = None

  def terminator(self, char, open):
    return  char == "." and self.peekChar() in string.whitespace and open == 0

  def getWord(self, acc = "", open = 0):
    char = self.readChar()

    while char != None:
      acc += char
       
      if self.terminator(char, open):
        c = self.readChar()
        if c is not None:
          acc += c
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
          if open == 0 and self.isComment(acc):
            while self.peekChar() in string.whitespace:
              c = self.readChar()
              if c is not None:
                acc += c
              else:
                # At end of text, peekChar will return whitespace, but readChar
                # returns None, so break out of loop.
                break

            return acc

      char = self.readChar()

    return acc
      
  def parse(self, buffer):
    self.script += buffer
    if self.unfinished:
      acc = self.unfinished
    else:
      acc = ""
    
    command = self.getWord(acc = acc)
    
    result = []
    while (len(command) != 0):
      if not (self.isCommand(command) or self.isComment(command)):
        self.unfinished = command
        command = ""

      else:
        self.unfinished = ""
        result.append(command)
        command = self.getWord()
    
    if self.unfinished:
      result.append(self.unfinished)
    
    return result

  def isComment(self, text):
    """ Return whether the given text is a comment. """
    return (len(text.strip()) <= 0 or
            (text.strip().startswith("(*") and text.strip().endswith("*)") and
             self._balanced_comments(text)))


  def _has_terminator(self, text):
    return text[-1] == '.' and (
               (text[-2] != '.' if len(text) >= 2 else True) 
            or (text[-3] == '.' if len(text) >= 3 else True))

  def _balanced_comments(self, text):
    """ Balanced comment tokens. """
    return text.count("(*") == text.count("*)")
  def isCommand(self, text):
    """ Return whether the given text is a Coq command. """
    text = text.rstrip()
    if text:
      return self._balanced_comments(text) and self._has_terminator(text)
  
  def _escape_to_html(self, text):
    """ Escape entities to (pre-formatted) HTML. """
    entities = {
      ' ' : '&nbsp;',
      '\n': '<br/>',
    }
  
    return escape(text, entities)

  def make_frames(self, prover = None):
    """ Splits the file stored in self.script into seperate commands, 
        and pairs these commands to their responses as provided by prover.

        Arguments:
        - prover: The prover to send commands to.
    """
    
    document = Movie()
    scene = Scene()
    scene.set_type("code")

    document.add_scene(scene)

    command = self.getWord()
    
    while command != None and len(command) != 0:
      if self.isComment(command):
        response = None
      else:
        response = prover.send(command)
      
      coqdoc_command = self._escape_to_html(command)
      f = Coqdoc_Frame(command = command, command_cd = coqdoc_command,
                           response = response)
      f.set_code(True)

      f.set_dependencies(self._deps)
      self._deps = [f]
      
      scene.add_scene(f)

      command = self.getWord()

    return document

