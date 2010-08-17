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

from xml.dom.minidom import Document, parse
from Frame import TAG_FRAME, Frame

TAG_FILM = "film"

class Movie:
  """ A data class for movies """
  
  def __init__(self):
    """ A movie gets  a list of frames. """
    # TODO Having both a list of frames (ordered) and a dictionary 
    # (unordered) is a bit unelegant. Better to have frameId -> frame
    # and an ordering on the individual frames. 
    # For now, however, this suffices.
    self._frames = []
    self._frameIds = {}
  
  def fromxml(self, document):
    """ Load the movie frames from the given xml document """
    
    film = document.getElementsByTagName(TAG_FILM)[0]
    frameElements = film.getElementsByTagName(TAG_FRAME)
    
    for element in frameElements:
      frame = Frame()
      frame.fromxml(element)
      self.addFrame(frame)

  def addFrame(self, frame):
    frame.setId(self.getLength())
    self._frames.append(frame)
    self._frameIds[frame.getId()] = self.getLength() - 1

  def removeFrame(self, frame):
    self._frames.remove(frame)

  def getLength(self):
    """ The length of a movie is the number of its frames """
    return len(self._frames)

  def getFrame(self, i):  
    return self._frames[i]

  def toxml(self, stylesheet="proviola.xsl"):
    """ Marshall the movie to an XML document. """
    doc = Document()

    styleSheetRef = doc.createProcessingInstruction("xml-stylesheet",\
                              "type=\"text/xsl\" href=\"%s\""%stylesheet)
    doc.appendChild(styleSheetRef)

    movie = doc.createElement("movie")
    doc.appendChild(movie)

    film = doc.createElement(TAG_FILM)
    movie.appendChild(film)
    
    for frame in self._frames:
      film.appendChild(frame.toxml(doc))
    
    return doc.toxml()

  def toFile(self, fileName, stylesheet = "proviola.xsl"):
    """ Write the file, in XML, to filmName """ 
    filmFile = open(fileName, 'w')

    filmFile.write(self.toxml(stylesheet))
    filmFile.close()

  def openFile(self, fileName):
    """ Open an XML file and load its data in memory. """
    doc = parse(fileName)
    self.fromxml(doc)

  def getFrameById(self, id):
    """ Return the frame identified by the given id. """
    return self.getFrame(self._frameIds[id])