#!/usr/bin/python3
#
# Author: Carst Tankink carst 'at' cs 'dot' ru 'dot' nl
# Copyright: Radboud University Nijmegen
#
# This file is part of the Coqdoc Pretty Printer.
#
# Coqdoc Pretty Printer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Coqdoc Pretty Printer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Coqdoc Pretty Printer.  If not, see <http://www.gnu.org/licenses/>.
from xml.dom.minidom import parse, parseString, Node
from xml.parsers.expat import ExpatError, ErrorString
import sys
import coqdocdriver

def getDocument(element):
  ''' Get the document for the given element.

  Arguments:
  - element: The element to find the document of.

  Returns:
  - The document root of element.
  '''

  while element.parentNode != None:
    element = element.parentNode

  return element

def parseArguments(argv):
  '''
  Parse arguments into filename of film to be processed and (optionally)
  film to be created

  Arguments:
  - argv: The arguments to be parsed. If None, this is taken from the 
          commands passed when calling the script
  
  Returns:
  - (film, newFile): argv[1] and argv[2]: the filename of the film to be 
                     parsed and the film written into. If argv[2] is 
                     non-existant, newFilm == film
  Raises
  - ValueError iff argv[1] is not provided.
  '''

  if argv is None:
    argv = sys.argv
  try:
    film = argv[1]
    try:
      newFile = argv[2]
    except IndexError:
      newFile = film
  except IndexError:
    raise ValueError("Too few arguments") 
  
  return (film, newFile)

def getClass(node):
  ''' Get the class of the given node

  Arguments
  - node: An XML DOM node.

  Returns:
  - The value of the ``class'' attribute of this node.
  '''
  return node.getAttribute('class')

def addReference(scene, frame, div):
  ''' Add a reference to the given frame to the given scene.
  
  Arguments:
  - scene: the scene that is to refer to the given frame.
  - frame: the frame to refer to.

  Result: Scene has a child referring to frame.
  '''
  if scene == None or getClass(scene) != getClass(div):
    scene = getDocument(frame).createElement("scene")
    scene.setAttribute("class", getClass(div))

    
  divReference = getDocument(frame).createElement("div-reference")
  divReference.setAttribute("frame", frame.getAttribute("frameNumber"))
  divReference.setAttribute("div", div.getAttribute("divNumber"))
  scene.appendChild(divReference)
  return scene

def groupIntoScenes(frames):
  ''' Create a list of scenes from the given frames.
  
  Arguments:
  - frames: The set of frames that needs to be grouped into scenes. We 
            assume each frame has a command-coqdoc element.
  Returns:
  - A list of <scene/> elements: each element contains a reference to each
    frame in frames that can logically be grouped: a scene corresponds to a
    (sub)section of the coq-doc file and can contain subscenes.
  '''
  
  document = getDocument(frames.item(0))
  scenes = document.createElement("scenes")
  document.documentElement.appendChild(scenes)
  
  scene = None
  for frame in frames:
    coqdoc = frame.getElementsByTagName('command-coqdoc')
    if len(coqdoc) == 1:
      coqdoc = coqdoc[0]
      coqdoc.normalize()

      for child in [c for c in coqdoc.childNodes\
                    if c.nodeType != Node.TEXT_NODE]:
        scene = addReference(scene, frame, child)
        # A bit wasteful, but saves some arguments
        scenes.appendChild(scene)
        scene.setAttribute("sceneNumber", "%d"%(len(scenes.childNodes) - 1))

  return scenes

def emptyDiv(node):
  ''' Determine if the given node is an ``empty'' code div.

  Arguments:
  - node: The node to be inspected.

  Result:
  - whether or not the node is a ``code'' div only containing newlines and
    a <br/> element.
  '''
  
  if node.nodeType == Node.TEXT_NODE:
    return True
  if getClass(node) == 'code':
    children = node.childNodes 
    if len(children) == 3 and \
       children.item(0).data == "\n\n" and \
       children.item(1).nodeName == "br" and \
       children.item(2).data == "\n":  
      return True
    elif len(children) == 1 and \
         children.item(0).data == "\n":
      return True

  return False

def cleanup(coqDocNode):
  ''' Remove these silly empty-code divs.

  Argument:
  - coqDocNode: A node as returned by coqDoc

  Result: 
  - coqDocNode has no empty code fragments.
  '''
  emptyChildren = []
  for child in coqDocNode.childNodes:
    if emptyDiv(child):
      emptyChildren.append(child)

  #Removing children on the fly messes up the iterator, so do it post-facto
  for child in emptyChildren:
    coqDocNode.removeChild(child)
    child.unlink()
  
  # remove trailing <br/> elements
  coqDiv = coqDocNode.firstChild
  if coqDiv != None and getClass(coqDiv) == "code":
    lastNode = coqDiv.lastChild
    while lastNode.nodeType == Node.TEXT_NODE:
      lastNode = lastNode.previousSibling
    if lastNode.tagName == "br":
      coqDiv.removeChild(lastNode)
      lastNode.unlink()

def makeCoqDoc(movie):
  ''' 
  Returns a new movie with a scene for each CoqDoc section. 

  Arguments:
  - movie: An XML movie document
  Returns:
  - coqDocMovie: movie, rendered by CoqDoc and grouped into scenes.
  '''
  
  frames = movie.getElementsByTagName("frame")
  driver = coqdocdriver.CoqDocDriver()

  for frame in frames:
    commands = frame.getElementsByTagName("command")
    assert(len(commands) == 1)
    text = commands[0].firstChild.data
    coqDoc = driver.process(text)
    coqDoc = '<command-coqdoc>' + coqDoc.decode() + "</command-coqdoc>"
    coqDoc = coqDoc.replace("&nbsp;", "&#160;")
#TODO Test to see if -2 caused the break -> It did. This is a temporary fix.
    coqDoc = coqDoc.replace("-2", "\"-2\"")
    try:
      coqDocElement = parseString(coqDoc).documentElement
    except ExpatError as e:
      print("Expat error:",ErrorString(e.code))
      print("String was:",coqDoc)
      break
      
    cleanup(coqDocElement)
    
    divNumber = 0
    for div in coqDocElement.childNodes:
      div.setAttribute("divNumber", "%d"%divNumber)
      divNumber += 1
  
    frame.appendChild(coqDocElement)

  groupIntoScenes(frames)
  return movie

def main(argv = None):
  (film, newFile) = parseArguments(argv)
  print("Processing:", film)
  original = parse(film)
  styleSheetRef = original.createProcessingInstruction("xml-stylesheet",\
                          "type=\"text/xsl\" href=\"proviola-coqdoc.xsl\"")  
  newFilm = makeCoqDoc(original)
  newFilm.insertBefore(styleSheetRef, newFilm.documentElement)
  newFilm.writexml(open(newFile, 'w'))

if __name__ == "__main__":
  sys.exit(main())
