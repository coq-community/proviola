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


import re
from Reader import Reader
import string
from Frame import Frame
from time import sleep
from ProofWeb import ProofWeb
suffix = '.v'

class CoqReader(Reader):
  def __init__(self, filename = ""):
    Reader.__init__(self)
    self.suffix = ".v"
    if filename != "":
      self.basename = filename[:-len(suffix)]
      self.read(filename)

  def coqUndot(self, scriptText):
    result = scriptText.replace("Undo.Undo", "Undo. ndo")
    result = result.replace("...", "__.") 
    result = result.replace("..", "__")
    result = re.sub(r'\.[a-zA-Z1-9_]', "AA", result)
    return result
  
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
    if char == ".":
      return self.peekChar() in string.whitespace and open == 0

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
    self.script = buffer
    command = self.getCommand()
    result = []
    while (len(command) != 0):
      result.append(command)
      command = self.getCommand()
    return result
  
  def makeFrames(self, document, options, remaining = ""):
    pw = ProofWeb(options.pwurl, options.group)
    command = self.getCommand()
    while command != None and len(command) != 0:
      if self.isComment(command):
        response = None
      else:
        response = pw.send(command)
      
      id = 0
      document.addFrame(Frame(id, command, response))
      sleep(.5)
      command = self.getCommand()
    
  def isComment(self, text):
    return len(text.split()) <= 0 or\
           text.split()[0].startswith("(*") and text.endswith("*)")
  
  def isCommand(self, text):
    return self.terminator(text[len(text) - 1], 0)
