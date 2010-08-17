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


from xml.dom.minidom import Document

class FilmDocument(Document):
  def __init__(self, styleSheetUrl="\"proviola.xsl" + "\""):
    Document.__init__(self)
    self.frameNumber = 0
    self.film = self.createElement("film")
    
    styleSheetRef = self.createProcessingInstruction("xml-stylesheet",\
                                                     "type=\"text/xsl\" href=" + styleSheetUrl)
    
    self.appendChild(styleSheetRef)
    
    movie = self.createElement("movie")
    self.appendChild(movie)
    movie.appendChild(self.film)

  def constructFrame(self, command, response, tagname = "frame"):
    frame = self.createElement(tagname)
    frame.setAttribute("frameNumber", "%s"%self.frameNumber)
    frame.appendChild(self.createTextElement("command", command))  
    frame.appendChild(self.createTextElement("response", response)) 
    return frame

  def constructRawFrame(self, command, response):
    return self.constructFrame(command, response, "rawFrame")
   
  def createTextElement(self, elementName, contents):
    element = self.createElement(elementName)
    text = self.createTextNode(contents)
    element.appendChild(text)
    return element 

  def addFrame(self, command, response):
    frame = self.constructFrame(command, response)
    self.film.appendChild(frame)
    self.frameNumber += 1
  
  def addRawFrame(self, command, response):
    frame = self.constructRawFrame(command, response)
    self.film.appendChild(frame)
    self.frameNumber += 1

  def writeFilm(self, fileName):
    filmFile = open(fileName, 'w')

    filmFile.write(self.toxml())
    filmFile.close()

  def tolist(self):
    result = []
    
    for frame in self.film.childNodes:
      result.append(frame.toxml())
    
    return result
