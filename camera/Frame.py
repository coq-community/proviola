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

from lxml import etree

TAG_FRAME = "frame"
TAG_ID = "framenumber"
TAG_CMD = "command"
TAG_RES = "response"
TAG_DEPS = "dependencies"
TAG_DEP  = "dependency"


class Frame:
  """ A class for frames """

  def __init__(self, id = -1, command = None, response = None):
    """ A frame always has an id and a command, but optionally a response 
    """
    self._id = id
    self._command = command 
    self._response = response
    self._processed = bool(response)
    
    self._is_code = False

    self._dependencies = []

  def get_dependencies(self):
    return self._dependencies

  def getCommand(self):
    """ Getter for the command field. """
    return self._command
  
  def set_command(self, cmd):
    """ Sets a command. """
    self._command = cmd

  def setId(self, id):
    self._id = id

  def set_number(self, number):
    """ Frames should not keep a scene-number """
    pass
  
  def set_response(self, response):
    """ Set the response in the frame. """
    self._response = response
    self._processed = True

  def getResponse(self):
    return self._response
  
  def is_processed(self):
    return self._processed

  def getId(self):
    return self._id
  
  def is_scene(self):
    return False

  def fromxml(self, elem):
    """ Fill frame from given elem. """
    self._id = elem[TAG_ID]

    if elem.command and elem.command.string:
      self._command = unescape(elem.command.string)
    else:
      self._command = ""

    if elem.response and elem.response.string:
      self._response = unescape(elem.response.string)
    
    dependencies = []
    for dep in (elem.dependencies or []):
      dependencies.append(int(dep[TAG_ID]))

    self.set_dependencies(dependencies)
  
  def toxml(self):
    """ To xml. """
    element  = etree.Element(TAG_FRAME)
    element.set(TAG_ID, str(self.getId()))
    
    command = etree.SubElement(element, TAG_CMD)
    command.text = self.getCommand()

    if self.getResponse():
      response = etree.SubElement(element, TAG_RES)
      response.text = self.getResponse()

    dependencies = etree.SubElement(element, TAG_DEPS)
    for dep in self.get_dependencies():
      dependency = etree.SubElement(dependencies, TAG_DEP)
      dependency.set(TAG_ID, str(dep))

    return element

  def createTextElement(self, doc, elementName, contents):
    """ Convenience method for creating text-containing nodes in doc """
    contents = contents or ""
    element = Tag(doc, elementName)
    element.append(escape(contents))
    return element 
  
  def get_reference(self):
    """ Give a reference to a frame, as its identifier. """
    element = etree.Element("frame-reference")
    element.set(TAG_ID, str(self.getId()))
    return element

  def set_dependencies(self, frames):
    """ Mark which frames this frame depends on. """
    self._dependencies = frames

  def flatten(self):
    return [self]
  
  def is_code(self):
    return self._is_code

  def set_code(self, is_code):
    self._is_code = is_code
