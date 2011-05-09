from os import makedirs
from os.path import exists, dirname

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
    
  def get_title(self):
    """ Returns the title of the movie. """
    return self._title
  
  def get_scenes(self):
    """ Getter for self._scenes. """
    return self._scenes
  
  def add_to_title(self, title):
    """ Add the argument to the title. """
    if title:
      self._title += title

  def toxml(self, stylesheet="proviola.xsl"):
    frame_doc = Movie.toxml(self, stylesheet)    
    frame_doc.insert(1, Declaration('DOCTYPE movie [<!ENTITY nbsp "&#160;">]'))
    
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

  def from_string(self, xml_string):
    """ Initialize movie from the given xml tree in string form.
    """
    tree = BeautifulStoneSoup(xml_string)
    return self.fromxml(tree)
  
  def _is_local(self, link):
    """ Test if a given link element is local or remote. """
    target = link.get("href") 
    return target and (not target.startswith("http://"))
  
  def toFile(self, file_name, stylesheet = "proviola.xsl"):
    """ Write the instance to file_name, replacing any internal links with 
        references to the written file. """
    xml = self.toxml(stylesheet) 
    links = xml.findAll(name = "a")
    
    for link in links:
      if self._is_local(link):
        url, hash, anchor = link["href"].partition("#")
        location, dot, _ = url.rpartition(".")
        _, dot, new_extension = file_name.rpartition(".")
        link["href"] = location + dot + new_extension + hash + anchor
    
    if not exists(dirname(file_name)):
      makedirs(dirname(file_name))
    open(file_name, 'w').write(str(xml))
    
  def _replace_frames(self, scene):
    """ Replace the frames in scene by the actual frames in the movie. """
    for sub in scene.get_subscenes():
      if sub.is_scene():
        self._replace_frames(sub)
      else:
        scene.replace_frame(sub, self.getFrameById(sub.getId()))
