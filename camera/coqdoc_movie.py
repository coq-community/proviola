
from external.BeautifulSoup import Tag, Declaration, BeautifulStoneSoup
BeautifulStoneSoup.NESTABLE_TAGS["scene"] = []

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
    """ Add given scene to the movie. """
    scene.set_number(len(self._scenes))
    self._scenes.append(scene)
  
  def get_scenes(self):
    """ Getter for self._scenes. """
    return self._scenes
 
  def toxml(self, stylesheet="proviola.xsl"):
    frame_doc = Movie.toxml(self, stylesheet)    
    
    scene_tree = Tag(frame_doc, "scenes")
    frame_doc.movie.append(scene_tree)
      
    for scene in self._scenes:
      scene_tree.append(scene.toxml(frame_doc))      
        
    return frame_doc

  def fromxml(self, xml):
    """ Unmarshall the given xml tree into a Coqdoc_movie. """
    self._frames = []
    self._scenes = []
    
    for frame_xml in xml.film.findAll(name="frame"):
      frame = Coqdoc_Frame()
      frame.fromxml(frame_xml)
      self.addFrame(frame)

    for scene_xml in xml.scenes.findAll(name="scene", recursive = False):
      scene = Scene()
      scene.fromxml(scene_xml)
      self._replace_frames(scene)
      self.add_scene(scene)

  def _replace_frames(self, scene):
    """ Replace the frames in scene by the actual frames in the movie. """
    for sub in scene.get_subscenes():
      if sub.is_scene():
        self._replace_frames(sub)
      else:
        scene.replace_frame(sub, self.getFrameById(sub.getId()))
