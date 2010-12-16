""" A parser for Coqdoc's HTML. """
from xml.dom.minidom import parseString, Node, parse

from BeautifulSoup import BeautifulSoup

import CoqReader
import coqdoc_movie
from Prover import get_prover

from coqdoc_frame import Coqdoc_Frame
from scene import Scene


class Coqdoc_Parser(object):
  def __init__(self):
    self._movie = None
    self._tree = None
    self._reader = CoqReader.CoqReader()
    self._prover = get_prover("http://hair-dryer.cs.ru.nl/proofweb/index.html",
                              "nogroup")
    
  def _clean_html(self, text):
    """ Replace HTML entities by their ASCII equivalents. 
    """
    replacements = {
          "&nbsp;": " ",
          "&gt;"  : ">",
          "&lt;"  : "<"}
    
    for key in replacements:
      text = text.replace(key, replacements[key])
      
    return text
  
  def _get_text(self, node):
    """ Get the text portion out of an HTML node. Special characters are still
        encoded as HTML entitites.
    """   
    try:
      return node.text
    except:
      return node
    
  def _hidden_span(self, div):
    # TODO: Make the hidden span an actual class...
    """ Recognizer for spans with the "display: none" style. """
    try:
      div.get("style") == "display: none"
    except AttributeError:
      return False
           
  def _process_code(self, code_div):
    """ Process a code div. 
        A code div corresponds to a single scene, refering to zero or more
        frames.
    """
    frames = []
    
    scene = Scene()
    scene.set_type("code")
    code_tree = []
    
    for child in code_div:
      if self._hidden_span(child):
          (hidden_frames, hidden_scenes) = self._process_code(child)
          hidden_scenes[0].set_type("hidden")
          scene.add_scene(hidden_scenes[0])
          frames += hidden_frames
          
      else:
        code_tree.append(child)
        commands = self._reader.parse(self._get_text(child))
        
        commands = [c for c in commands if self._reader.isCommand(c) or
                                           self._reader.isComment(c)]
        
        if len(commands) == 1:
          cmd = commands[0]
          cmd_clean = self._clean_html(cmd)
          if self._reader.isCommand(cmd_clean):
            response = self._prover.send(cmd_clean)
          else:
            response = None
          
          
          frame = Coqdoc_Frame(command = cmd, 
                               command_cd = code_tree,
                               response = response)
          
          scene.add_scene(frame)
          frames.append(frame)
      
          code_tree = []
          
        elif len(commands) > 1:       
          print "More commands: ", `commands`
          
    return (frames, [scene])
    
  
  def _html_to_frame(self, node):
    """ Process plain html. """
    # TODO: Better to specify an actual invert for CoqDoc comments. 
    frame = Coqdoc_Frame(command = "(*" + self._get_text(node) + "*)",
                         command_cd = [node], response = None)
      
    return frame  
             
  def _process_div(self, div = None):
    """ Process a div, translated to a scene. """
    if div.get("class") == "code":
      return self._process_code(div)
      
    else:
      # TODO: Process.
      scene = Scene()
      scene.set_type("doc")
      scene.set_attributes(div.attrs)
      frames = []
      
      for child in div:
        try:
          if child.name == "div":
              (div_frames, div_scenes) = self._process_div(child)    
              frames += div_frames
              for div_scene in div_scenes:
                scene.add_scene(div_scene)
              
          else:  
            # TODO: Better to specify an actual invert for CoqDoc comments. 
            frame = self._html_to_frame(child)
            frames.append(frame)  
            scene.add_scene(frame)
            
        except:
            frame = self._html_to_frame(child)
            frames.append(frame)
            scene.add_scene(frame)
            
      return (frames, [scene])
  
  def _process_body(self, body):
    """ Extract scenes and frames from the body element given.
        
        Arguments:
        - body: The body element of a Coqdoc-generated HTML file.
        
        Returns:
        - (frames, scenes): A list of frames and a list of scenes, such that the 
              Coqdoc file can be (morally) reconstructed by following the 
              references in each of the scenes.
    """
    frames = []
    scenes = []
        
    for div in body.findChildren(name = "div", recursive = False):
      (div_frames, div_scenes) = self._process_div(div)
      frames += div_frames
      scenes += div_scenes
    
    return (frames, scenes)
  
  def _tree_to_movie(self, tree):
    """ Transform the Coqdoc-generated HTML tree into a Coqdoc-enhanced movie.
    
      Arguments:
      - tree: The HTML tree used as data source. (default: the Tree stored in 
              the parser)
      Returns:
        m = coqdoc_movie.Coqdoc_movie s.t. it is possible to extract the tree 
                                           from m.
    """
    movie = coqdoc_movie.Coqdoc_Movie()    
    movie.add_to_title(tree.html.head.title.string)
    (frames, scenes) = self._process_body(tree.html.body)  
        
    for scene in scenes:
      movie.add_scene(scene)
    for frame in frames:
      movie.addFrame(frame)
    
    return movie
    
  def feed(self, data):
    """ 
    Feed data to the parser

    Arguments:
    - data: An string describing the XML tree to parse.
    
    Effect: self._coqdoc_movie is updated with the contents of data. 
    """
    
    self._tree = BeautifulSoup(data)
    
    self._movie = self._tree_to_movie(self._tree)
    
  def get_coqdoc_movie(self):
    return self._movie
