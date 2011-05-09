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

from xml.sax.saxutils import escape, unescape
from external.BeautifulSoup import Tag


TAG_FRAME = "frame"
TAG_ID = "framenumber"
TAG_CMD = "command"
TAG_RES = "response"

class Frame:
  """ A class for frames """

  def __init__(self, id = -1, command = None, response = None):
    """ A frame always has an id and a command, but optionally a response 
    """
    self._id = id
    self._command = command
    self._response = response


  def getCommand(self):
    """ Getter for the command field. """
    return self._command

  def setId(self, id):
    self._id = id


  def getResponse(self):
    return self._response

  def getId(self):
    return self._id
 
  def fromxml(self, elem):
    """ Fill frame from given elem. """
    self._id = elem["framenumber"]
    
    if elem.command and elem.command.string:
      self._command = unescape(elem.command.string)
    
    if elem.response and elem.response.string:
      self._response = unescape(elem.response.string)

  def toxml(self, doc):
    frameElement = Tag(doc, TAG_FRAME)
    frameElement[TAG_ID] = self.getId()
    frameElement.append(self.createTextElement(doc, TAG_CMD,
                                            self.getCommand()))

    if self._response:
      frameElement.append(self.createTextElement(doc, TAG_RES, 
                                            self.getResponse()))
    
    return frameElement 

  
  def createTextElement(self, doc, elementName, contents):
    """ Convenience method for creating text-containing nodes in doc """
    contents = contents or ""
    element = Tag(doc, elementName)
    element.append(escape(contents))
    return element 

  def get_reference(self,document):
    """ A Frame is referred to by its identifier. """
    
    ref = Tag(document, "frame-reference")
    ref[TAG_ID] = self.getId()
    return ref
