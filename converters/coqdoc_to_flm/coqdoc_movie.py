from BeautifulSoup import Tag, Declaration
from Movie import Movie

from coqdoc_frame import Coqdoc_Frame
from scene import Scene

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
  
  def get_scenes(self):
    """ Getter for self._scenes. """
    return self._scenes
  
  def add_to_title(self, title):
    """ Add the argument to the title. """
    if title:
      self._title += title

  def toxml(self):
    frame_doc = Movie.toxml(self)
    
    frame_doc.insert(1, Declaration('DOCTYPE movie [<!ENTITY nbsp "&#160;">]'))
    doc_root = frame_doc.movie
    
    scene_tree = Tag(frame_doc, "scenes")
    doc_root.append(scene_tree)
    
    for scene in self._scenes:
      scene_tree.append(scene.toxml(frame_doc))

    return frame_doc

  def fromxml(self, xml):
    """ Unmarshall the given xml tree into a Coqdoc_movie. """
    for frame_xml in xml.film:
      frame = Coqdoc_Frame()
      frame.fromxml(frame_xml)
      self.addFrame(frame)

    for scene_xml in xml.scenes:
      scene = Scene()
      scene.fromxml(scene_xml)
      self.add_scene(scene)
