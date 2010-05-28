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


class Frame:

  """ A data class for frames """

  def __init__(self, id, command, response = None):
    """ A frame always has an id and a command, but optionally a response 
    """
    self._id = id
    self._commad = command
    self._response = response

  def getCommand(self):
    return self._command

  def hasResponse(self):
    return self._response != None
    
  def getResponse(self):
    return self._response

  def getId(self):
    return self._id
