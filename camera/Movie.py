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

from external.BeautifulSoup import BeautifulStoneSoup 
from external.BeautifulSoup import Tag, Declaration, ProcessingInstruction

from lxml import etree
from StringIO import StringIO

from os import makedirs
from os.path import exists, dirname


from frame_factory import make_frame
from scene import Scene
BeautifulStoneSoup.NESTABLE_TAGS["scene"] = []


TAG_FILM = "film"

class Movie(object):
  """ A data class for movies """
  
  def __init__(self):
    """ A movie gets  a list of frames. """
    # TODO Having both a list of frames (ordered) and a dictionary 
    # (unordered) is a bit unelegant. Better to have frameId -> frame
    # and an ordering on the individual frames. 
    # For now, however, this suffices.
    self._frames = []
    self._frameIds = {}
    
    self._scenes = []
    self._stylesheet = "proviola.xsl"
    self._title = ""
 
  def set_title(self, title):
    """ Sets the argument to the title. """
    if title:
      self._title = title

  def get_title(self):
    """ Getter for title. """
    return self._title

  def fromxml(self, document):
    """ Load the movie frames from the given xml document """
    self._frames = []
    self._scenes = []

    for element in document.film.findAll(name="frame"):
      frame = make_frame(element)
      self.addFrame(frame)

    for scene_xml in document.scenes.findAll(name="scene", recursive = False):
      scene = Scene()
      scene.fromxml(scene_xml)
      self._replace_frames(scene)
      self.add_scene(scene)

  def _get_dependencies(self):
    """ Get the tip of the dependency-tree (just the last frame in the movie.
    """ 
    frames = [f for f in self.get_frames() if f.is_code()]
    if frames:
      return [frames[-1]]
    else:
      return []



  def add_frame(self, frame):
    """ Rename of addFrame. """
    self.addFrame(frame)

  def addFrame(self, frame):
    """ Add frame to the movie. """ 
    frame.set_dependencies([f.getId() for f in self._get_dependencies()])
    frame.setId(self.getLength())

    self._frames.append(frame)
    self._frameIds[frame.getId()] = self.getLength() - 1

  def removeFrame(self, frame):
    self._frames.remove(frame)
  
  def get_frames(self):
    return self._frames

  def getLength(self):
    """ The length of a movie is the number of its frames """
    return len(self._frames)

  def getFrame(self, i):  
    return self._frames[i]

  def _add_PIs(self, document, stylesheet):
    """ Add XML processing instructions to the given document. """
    document.insert(0,
      ProcessingInstruction("xml version='1.0' encoding='utf-8'"))

    document.append(
      ProcessingInstruction(
        'xml-stylesheet type="text/xsl" href="%s"'%stylesheet))
  
  def from_string(self, xml_string):
    """ Initialize movie from the given xml tree in string form.
    """
    tree = BeautifulStoneSoup(xml_string, selfClosingTags=["dependencies"])
    return self.fromxml(tree)
  
  def _doctype(self):
    """ Returns the entity map as a string. """
    entity_map = {
      "nbsp":   "&#160;",
      "mdash":  "&#8212;",
      "dArr":   "&#8659;",
      "rArr":   "&#8658;",
      "rarr":   "&#8594;",
      "larr":   "&#8592;",
      "harr":   "&#8596;",
      "forall": "&#8704;",
      "exist":  "&#8707;",
      "exists": "&#8707;",
      "and":    "&#8743;",
      "or":     "&#8744;",
      "Gamma":  "&#915;",
    }

    entities = "\n".join(['<!ENTITY %s "%s">'%(key, entity_map[key]) 
                      for key in entity_map])
    return "<!DOCTYPE movie [{entities}]>".format(entities = entities)

 
  def toxml(self, stylesheet="proviola.xsl"):
    """ Export to XML. """
    self._stylesheet = stylesheet

    root = etree.Element("movie")

    root.set("title", self._title)
    
    film = etree.SubElement(root, "film")
    for frame in self._frames:
      film.append(frame.toxml())

    scenes = etree.SubElement(root, "scenes")
    for scene in self._scenes:
      scenes.append(scene.toxml())

    return root 
  
  def __str__(self):
    """ To string returns the XML version of the movie. """

    return etree.tostring(self.toxml(self._stylesheet), xml_declaration=True,
                          doctype = self._doctype())
                          

  def toFile(self, file_name, stylesheet = "proviola.xsl"):
    """ Write the file, in XML, to filmName """
    
    self._stylesheet = stylesheet

    if len(dirname(file_name)) > 0 and not exists(dirname(file_name)):
      makedirs(dirname(file_name))
    
    f = open(file_name, 'w')
    f.write(str(self))
    f.close()


  def openFile(self, fileName):
    """ Open an XML file and load its data in memory. """
    doc = BeautifulStoneSoup(open(fileName, 'r').read())

    self.fromxml(doc)

  def getFrameById(self, id):
    """ Return the frame identified by the given id. """
    try:
      return self.getFrame(self._frameIds[int(id)])
    except KeyError:
      return None


  def add_scene(self, scene):
    """ Add given scene to the movie. """
    scene.set_number(len(self._scenes))
    self._scenes.append(scene)

  def get_scenes(self):
    """ Getter for self._scenes. """
    return self._scenes
 
  def _replace_frames(self, scene):
    """ Replace the frames in scene by the actual frames in the movie. """
    for sub in scene.get_subscenes():
      if sub.is_scene():
        self._replace_frames(sub)
      else:
        scene.replace_frame(sub, self.getFrameById(sub.getId()))

  def __len__(self):
    return len(self._frames)
