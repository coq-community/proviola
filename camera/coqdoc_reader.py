""" Implements a Reader class for Coqdoc documents. """

from CoqReader import CoqReader
from coqdoc_movie import Coqdoc_Movie
from scene import Scene
from coqdoc_frame import Coqdoc_Frame

from external.BeautifulSoup import BeautifulSoup

suffix = ".html"

class Coqdoc_Reader(CoqReader):
  """ Reader that reads Coqdoc-produces HTML files, creating a movie maintaining
      the original layout, with state output inlined.
  """
  
  def __init__(self):
    """ Setup: creates an empty movie. """
    CoqReader.__init__(self)
    self._movie = Coqdoc_Movie()
    self._prover = None
    
  def add_code(self, code):
    """ Override of the corresponding method in Reader: makes a 
        BeautifulSoup tree out of the given Coqdoc document. """
        
    self._coqdoc_tree = BeautifulSoup(code)
  
  def _find_commands(self, div):
    """ Find the commands. This is a wrapper around parent's parse. """
    try:
      text = div.text
    except:
      text = div
      
    return self.parse(text)
  
  def _replace_html(self, text):
    """ Replace HTML entitities by ASCII equivalents. """
    replacements = {
          "&nbsp;": " ",
          "&gt;"  : ">",
          "&lt;"  : "<"}
    
    for key in replacements:
      text = text.replace(key, replacements[key])
      
    return text
  
  def _process_code(self, div):
    """ Process a code div, returning a scene and the frames referenced.
    """
    frames = []
  
    scene = Scene()
    scene.set_type("code")
    
    coqdoc = ""
    for child in div:
      coqdoc += str(child)
      commands = self._find_commands(child)
      if commands and self.isCommand(commands[0]): 
        command = self._replace_html(commands[0])
        response = self._prover.send(command)
        frame = Coqdoc_Frame(command = command, command_cd = coqdoc,
                           response = response)
        frames.append(frame)
        scene.add_scene(frame)
        
        coqdoc = ""
    
    trailing_frame = Coqdoc_Frame(command = coqdoc, 
                                  command_cd = coqdoc,
                                  response = None)
    frames.append(trailing_frame)
    scene.add_scene(trailing_frame)
    
    return frames, scene
  
  def _process_doc(self, div):
    frames = []
    scene = Scene()
    scene.set_type("doc")
    scene.set_attributes(div.attrs)
    
    for child in div:
      try:
        if child.name == "div": 
          child_frames, child_scene = self._process_div(child)
        else:
          child_scene = Coqdoc_Frame(command = child.text, command_cd = child,
                               response = None)
          child_frames = [child_scene]
      except AttributeError:
        child_scene = Coqdoc_Frame(command = child, command_cd = child,
                             response = None)
        child_frames = [child_scene]
      finally: 
        frames += child_frames
        scene.add_scene(child_scene)
          
    return frames, scene

  def _process_div(self, div):
    """ Given a div element, return a list of frames with the div's content, 
        and a scene mimicking its structure.  """
    
    if div.get("class") == "code":
      return self._process_code(div)
    else: 
      return self._process_doc(div)
      
    
  def make_frames(self, prover):
    """ Constructor of frames: reads the given HTML file (self.script) and 
        produces a frame per command/comment.
        
        - prover: handle to the prover to use to generate output. 
    """
    self._prover = prover
    
    try:
      self._movie.add_to_title(self._coqdoc_tree.head.title.text)
    except AttributeError:
      self._movie.add_to_title("")
    
    
    body = self._coqdoc_tree.body
    
    if body:
      for div in body.findChildren(name = "div", recursive = False):
        (frames, scene) = self._process_div(div)
          
        for frame in frames:
          self._movie.addFrame(frame)
          
        self._movie.add_scene(scene)
        
    return self._movie