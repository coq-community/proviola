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

class Movie:

  """ A data class for movies """
  
  def __init__(self):
    """ A movie gets  a list of frames. """
    self._frames = []

  def addFrame(self, frame):
    self._frames.append(frame)

  def removeFrame(self, frame):
    self._frames.remove(frame)

  def getLength(self):
    """ The length of a movie is the length of its frames """
    return len(self._frames)

  def getFrame(self, i):  
    return self._frames[i]

  def toxml():
    """ Marshall the movie to an XML document. """
    doc = Document()

    styleSheetRef = doc.createProcessingInstruction("xml-stylesheet",\
                              "type=\"text/xsl\" href=\"moviola.xsl\"")
    doc.appendChild(styleSheetRef)

    movie = doc.createElement("movie")
    doc.appendChild(movie)

    film = doc.createElement("film")
    movie.appendChild(film)
    
    for frame in self.frames:
      # TODO: Append the frames (as XML nodes) to the film
      frame = doc.createElement("frame")
      frame.setAttribute("frameNumber", "%s"%frame.getId())
      frame.appendChild(doc.createTextElement("command", frame.getCommand())

      if frame.hasResponse():
        frame.appendChild(doc.createTextElement("response", 
                                                frame.getResponse())

      film.appendChild(frame)

    return film.toxml()
