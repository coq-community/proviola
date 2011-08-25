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
  
  def get_scenes(self):
    """ Getter for self._scenes. """
    return self._scenes
  
  def toxml(self, stylesheet="proviola.xsl"):
    frame_doc = Movie.toxml(self, stylesheet)    
    # Entitites taken from Symbols.v in the SF notes.
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

    entities = "\n".join(
                ['<!ENTITY %s "%s">'%(key, entity_map[key]) 
                 for key in entity_map])
    frame_doc.insert(1, Declaration("DOCTYPE movie [" + entities + "]"))
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
    if len(dirname(file_name)) > 0 and not exists(dirname(file_name)):
      makedirs(dirname(file_name))
    open(file_name, 'w').write(str(xml))
    
  def _replace_frames(self, scene):
    """ Replace the frames in scene by the actual frames in the movie. """
    for sub in scene.get_subscenes():
      if sub.is_scene():
        self._replace_frames(sub)
      else:
        scene.replace_frame(sub, self.getFrameById(sub.getId()))
