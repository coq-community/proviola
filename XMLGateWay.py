#!/usr/bin/python
'''
Created on Jan 13, 2010

@author: carst
'''


import time

from xml.dom import minidom

from Film import FilmDocument
from CoqReader import CoqReader
from ProofWeb import ProofWeb
from DocXMLRPCServer import DocXMLRPCServer

class CameraServer:
  def __init__(self):
    self.payloadTag = "command"
    self.proofWeb = ProofWeb("http://hair-dryer.cs.ru.nl/proofweb/index.html")
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

if __name__ == '__main__':
  server = DocXMLRPCServer(("", 8000), logRequests = 0)
  server.register_introspection_functions()
  server.register_instance(CameraServer())
  
  print time.asctime(), "Application starting"
  server.serve_forever()
  print time.asctime(), "Application stopping"
  
