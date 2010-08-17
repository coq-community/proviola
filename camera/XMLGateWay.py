#!/usr/bin/python
#
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


'''
Created on Jan 13, 2010

@author: carst
'''

import time

from xml.dom import minidom

from FilmDocument import FilmDocument
from CoqReader import CoqReader
from ProofWeb import ProofWeb
from DocXMLRPCServer import DocXMLRPCServer

class CameraServer:
  def __init__(self):
    self.payloadTag = "command"
    self.url = "http://hair-dryer.cs.ru.nl/proofweb/index.html"
    self.proofWeb = ProofWeb(self.url)
    self.reader = CoqReader()
  
  def newFilm(self):
    self.film = FilmDocument()
    return True

  def sendFrame(self, frame):
    xmlFrame = minidom.parseString(frame)
    data = xmlFrame.getElementsByTagName(self.payloadTag)
    payload = data[0].firstChild.data
    
    for command in self.reader.parse(payload):
      if self.reader.isCommand(command):
        self.film.addFrame(command, "")
      else:
        self.film.addRawFrame(command, "")
     
    return self.film.tolist()  

  
  def createFilm(self, script):
    """ Create an entire film from a script, returning it as an XML tree 
    """
    self.newFilm()
    self.proofWeb = ProofWeb(self.url)
    self.reader.script = script
    
    self.reader.makeFrames(self.film, self.proofWeb)
    return self.film.toxml()

if __name__ == '__main__':
  server = DocXMLRPCServer(("", 8000), logRequests = 0)
  server.register_introspection_functions()
  server.register_instance(CameraServer())
  
  print time.asctime(), "Application starting"
  server.serve_forever()
  print time.asctime(), "Application stopping"
  
