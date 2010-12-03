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
import logging
from BeautifulSoup import Tag

TAG_FRAME = "frame"
TAG_ID = "frameNumber"
TAG_CMD = "command"
TAG_RES = "response"

class Frame:
  """ A class for frames """

  def __init__(self, id = 0, command = None, response = None):
    """ A frame always has an id and a command, but optionally a response 
    """
    self._id = id
    self._command = command
    self._response = response

  def getCommand(self):
    return self._command

  def setId(self, id):
    self._id = id

  def hasResponse(self):
    return self._response != None
    
  def getResponse(self):
    return self._response

  def getId(self):
    return self._id
 
  def getText(self, element, tagname):
    child = element.getElementsByTagName(tagname)[0].firstChild
    if child == None:
      return ""
    else:
      return child.data

  def fromxml(self, element):
    """ Populate this element from the given XML frame element. """
    try:
      self._id = element.getAttribute(TAG_ID)
      self._command = self.getText(element, TAG_CMD)
      
      if len(element.getElementsByTagName(TAG_RES)) > 0:
        self._response=  self.getText(element, TAG_RES)

    except IndexError as e:
      logging.debug("This frame has no id, name, was: ", element.toprettyxml("  "))
      raise e
    
  def toxml(self, doc):
    frameElement =Tag(doc, "temp_name")
    frameElement.name = TAG_FRAME
    frameElement[TAG_ID] = self.getId()
    frameElement.append(self.createTextElement(doc, TAG_CMD,
                                            self.getCommand()))

    if self.hasResponse():
      frameElement.append(self.createTextElement(doc, TAG_RES, 
                                                        self.getResponse()))
    
    return frameElement 

  def createTextElement(self, doc, elementName, contents):
    """ Convenience method for creating text-containing nodes in doc """
    element = Tag(doc, elementName)
    element.append(contents)
    return element 

  def get_reference(self,document):
    """ A Frame is referred to by its identifier. """
    
    ref = Tag(document, "frame-reference")
    ref[TAG_ID] = self.getId()
    return ref