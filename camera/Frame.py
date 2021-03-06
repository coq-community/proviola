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
import uuid
from lxml import etree

TAG_FRAME = "frame"
TAG_ID = "framenumber"
TAG_CMD = "command"
TAG_RES = "response"
TAG_DEPS = "dependencies"
TAG_DEP  = "dependency"


class Frame(object):
  """ A class for frames """

  def __init__(self, id = -1, command = None, response = None):
    """ A frame always has an id and a command, but optionally a response 
    """
    if id == -1:
      self._id = uuid.uuid4()
    else:
      self._id = id

    self._command = command 
    self._response = response
    self._processed = bool(response)
    self.__post_state = -1
    
    self._is_code = False

    self._dependencies = []
    
  def __eq__(self, other):
    """ Comparison based on attributes. """
    return self.__dict__ == other.__dict__

  def get_post(self):
    return self.__post_state

  def set_post(self, st):
    self.__post_state = st

  post_state = property(get_post, set_post)

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
    self._id = elem.get(TAG_ID)
    self.set_code(elem.get("is_code", default=False))

    if elem.find("./command") is not None and elem.find("./command").text:
      self._command = elem.find("./command").text
    else:
      self._command = ""

    if elem.find("./response") is not None and elem.find("./response").text:
      self._response = elem.find("./response").text
    
    dependencies = []
    deps = elem.find("./dependencies")
    for dep in (deps if deps is not None else []):
      dependencies.append(dep.get(TAG_ID))

    self.set_dependencies(dependencies)
  
  def toxml(self):
    """ To xml. """
    element  = etree.Element(TAG_FRAME)
    element.set(TAG_ID, str(self.getId()))
    if self.is_code():
      element.set("is_code", "true")

    command = etree.SubElement(element, TAG_CMD)
    cmd = self.getCommand()
    if cmd:
      if type(cmd) != type(u""):
        cmd = unicode(cmd, 'utf-8')
      command.text = cmd

    response = etree.SubElement(element, TAG_RES)
    resp = self.getResponse()
    if resp:
      if type(resp) != type(u""):
        resp = unicode(resp, 'utf-8', errors="ignore")
      response.text = resp

    dependencies = etree.SubElement(element, TAG_DEPS)
    for dep in self.get_dependencies():
      dependency = etree.SubElement(dependencies, TAG_DEP)
      dependency.set(TAG_ID, str(dep.getId()))

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
