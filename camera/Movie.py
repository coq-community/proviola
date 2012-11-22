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

from lxml import etree
from cStringIO import StringIO

from os import makedirs
from os.path import exists, dirname

from frame_factory import make_frame
from Frame import TAG_ID
from scene import Scene


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

  def _frame_from_xml(self, element):
    frame = make_frame(element)
    frame.set_dependencies([self.getFrameById(id) for id in
                            frame.get_dependencies()])
    return frame

  def fromxml(self, document):
    """ Load the movie frames from the given xml document """
    self._scenes = []


    for scene_xml in document.findall(".//scenes/scene"):
      scene = Scene()
      scene.fromxml(scene_xml)
      self._replace_frames(scene, document)
      self.add_scene(scene)

  def _get_dependencies(self):
    """ Get the tip of the dependency-tree (just the last frame in the movie.
    """ 
    frames = [f for f in self.get_frames() if f.is_code()]
    if frames:
      return [frames[-1]]
    else:
      return []

  def get_frames(self):
    return [f for s in self._scenes for f in s.flatten()]

  def getLength(self):
    """ The length of a movie is the number of its frames """
    return len(self.get_frames())

  def getFrame(self, i):  
    return self.get_frames()[i]

  def from_string(self, xml_string):
    """ Initialize movie from the given xml tree in string form.
    """
    tree = etree.parse(StringIO(xml_string))
    return self.fromxml(tree)
  
  def _doctype(self):
    """ Returns the entity map as a string. """
    return "<!DOCTYPE movie >"

  def toxml(self, stylesheet="proviola.xsl"):
    """ Export to XML. """
    self._stylesheet = stylesheet

    root = etree.Element("movie")

    root.set("title", self._title)
    
    film = etree.SubElement(root, "film")
    for frame in self.get_frames():
      film.append(frame.toxml())

    scenes = etree.SubElement(root, "scenes")
    for scene in self._scenes:
      scenes.append(scene.toxml())

    return root

  def _get_stylesheet_dec(self):
    return etree.ProcessingInstruction("xml-stylesheet",
                                       'href="{url}"'.format(url=self._stylesheet))
  def __str__(self):
    """ To string returns the XML version of the movie. """
    xml_string = etree.tostring(self.toxml(), xml_declaration=True,
                                doctype=self._doctype())

    doc = etree.parse(StringIO(xml_string))
    doc.getroot().addprevious(self._get_stylesheet_dec())
    return etree.tostring(doc, xml_declaration=True)
                          

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
    doc = etree.parse(fileName)
    self.fromxml(doc)

  def getFrameById(self, id):
    """ Return the frame identified by the given id. """
    for frame in self.get_frames():
      if frame.getId() == id:
        return frame

    return None

  def add_scene(self, scene):
    """ Add given scene to the movie. """
    scene.set_number(len(self._scenes))
    self._scenes.append(scene)

  def get_scenes(self):
    """ Getter for self._scenes. """
    return self._scenes
 
  def _replace_frames(self, scene, document):
    """ Replace the frames in scene by the actual frames in the movie. """
    for sub in scene.get_subscenes():
      if sub.is_scene():
        self._replace_frames(sub, document)
      else:
        frame_xml = document.find(".//film/frame[@{tag}='{id}']".format(
            tag=TAG_ID, id=sub.getId()))
        frame = self._frame_from_xml(frame_xml)
        scene.replace_frame(sub, frame)

  def __len__(self):
    return len(self.get_frames())
