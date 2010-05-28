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


from FilmDocument import FilmDocument

class Reader:
  def __init__(self):
    self.script = ""
    self.line = ""

  def getLine(self):
    if self.line == "":
      self.line = self.getNextLine()

  def appendData(self, pw, data):
    document = FilmDocument()
    print "Appending", data
    self.script += data
    self.makeFrames(document, pw)
    return document.toxml()
    
  def findNewLine(self):
    if self.script == None:
      return -1
    
    return self.script.find("\n")

  def read(self, filename):
    file = open(filename, 'r')
    self.script = file.read()
    file.close()
    
  def getNextLine(self):  
    if self.findNewLine() >= 0:
      result = self.script[0:self.findNewLine() + 1]
      self.script =  self.script[self.findNewLine() + 1 :]
      
    else:
      result = self.script
      self.script = "" 
    return result  
    
  def readChar(self):
    self.getLine()
    if len(self.line) == 0:
      return None
    
    char = self.line[0]
    self.line = self.line[1:]
    return char
  
  def peekChar(self):
    self.getLine()
    if len(self.line) > 0:
      return self.line[0]
    else:
      return ' '
    
      
import CoqReader
def getReader(filename):
  coqSuffix = CoqReader.suffix
  
  if filename.endswith(coqSuffix):
    return CoqReader.CoqReader(filename)

