from xml.dom.minidom import parseString

from Movie import Movie

from coqdoc_frame import Coqdoc_Frame

class Coqdoc_Movie(Movie):
  """ A coqdoc movie is a movie enhanced with scenes. """
  
  def __init__(self):
    """ Initialize an empty Movie. """
    Movie.__init__(self)

    self._title = ""
    self._scenes = []

  def add_scene(self, scene):
    scene.set_number(len(self._scenes))
    self._scenes.append(scene)

  def add_to_title(self, title):
    self._title += title

  def toxml(self):
    frame_doc = parseString(Movie.toxml(self).encode("ascii", "xmlcharrefreplace"))
    
    doc_root = frame_doc.documentElement
    scene_tree = frame_doc.createElement("scenes")
    doc_root.appendChild(scene_tree)
    
    for scene in self._scenes:
      scene_tree.appendChild(scene.toxml(frame_doc))

    return frame_doc