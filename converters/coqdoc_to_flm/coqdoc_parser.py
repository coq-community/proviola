""" A parser for Coqdoc's HTML. """
from xml.dom.minidom import parseString, Node, parse

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
    
  def _is_element(self, node):
    """ Recognizer for elements. """
    return node.nodeType == Node.ELEMENT_NODE
  
  def _is_head(self, node):
    """ Recognizer for head elements. """
    return node.tagName == "head"
  
  def _is_body(self, node):
    """ Recognizer for body elements. """
    return node.tagName == "body"
  
  
  def _is_div(self, node):
    """ Recognizer for div elements. """
    return self._is_element(node) and node.tagName == "div"
  
  def _extract_title(self, head):
    """ Extract the contents of the title child of the given head element.
    
      Arguments:
      - head: The head element containing the title.
      
      Returns:
      - title: The text inside the (unique) title element inside the head. 
    """    
    return head.getElementsByTagName("title")[0].firstChild.data
  
  def _is_code_div(self, div):
    """ Recognizer for divs with class "code" 
    """
    return self._is_div(div) and div.getAttribute("class") == "code"
  
  def _is_text(self, node):
    """ Recognizer for text nodes. """
    return node.nodeType == Node.TEXT_NODE
  
  def _get_text(self, node):
    """ Get the text grandchildren of given node. """
    if self._is_text(node):
      return node.data
    
    else:
      txt = ""
      for child in node.childNodes:
        txt += self._get_text(child)
        
      return txt
    
  def _hidden_span(self, div):
    """ Recognizer for spans with the "display: none" style. """
    return self._is_element(div) and div.tagName == "span" and\
           div.getAttribute("style").find("display: none") >= 0
           
  def _process_code(self, code_div):
    """ Process a code div. 
        A code div corresponds to a single scene, refering to zero or more
        frames.
    """
    
    frames = []
    
    scene = Scene()
    scene.set_type("code")
    
    code_tree = ""
    plain_code = ""
    for child in code_div.childNodes:
      if self._hidden_span(child):
          (hidden_frames, hidden_scenes) = self._process_code(child)
          hidden_scenes[0].set_type("hidden")
          scene.add_scene(hidden_scenes[0])
          frames += hidden_frames
      else:
        code_tree += child.toxml()
        commands = self._reader.parse(self._get_text(child))
        
        if len(commands) == 1 and self._reader.isCommand(commands[0]):
          
          frame = Coqdoc_Frame(command = commands[0], command_cd = code_tree,
                               response = self._prover.send(commands[0]))
          
          scene.add_scene(frame)
          frames.append(frame)
          
          code_tree = ""
          plain_code = ""
          
        elif len(commands) > 1:       
          print "More commands: ", `commands`
          print "Code tree: ", code_tree
    
    return (frames, [scene])
    
    
         
  def _process_div(self, div):
    """ Process a div, translated to a scene. """

    
    if self._is_code_div(div):
      return self._process_code(div)
      
    else:
      # TODO: Process.
      scene = Scene()
      scene.set_type("doc")
      scene.set_attributes(div.attributes)
      frames = []
      
      for child in div.childNodes:
        if self._is_div(child):
          (div_frames, div_scenes) = self._process_div(child)
        
          frames += div_frames
          for div_scene in div_scenes:
            scene.add_scene(div_scene)
        else: 
          # TODO: Better to specify an actual invert for CoqDoc comments. 
          frame = Coqdoc_Frame(command = "(*" + self._get_text(child) + "*)",
                               command_cd = child.toxml(), response = None)
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
    
    for child in [c for c in body.childNodes if self._is_element(c)]:
      if self._is_div(child):
        (div_frames, div_scenes) = self._process_div(child) 
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
    
    # First, normalize the tree
    tree.normalize()
    
    
    for child in [c for c in tree.documentElement.childNodes\
                    if self._is_element(c)]:
      if self._is_head(child):
        movie.add_to_title(self._extract_title(child))
               
      elif self._is_body(child):
        (frames, scenes) = self._process_body(child)  
        
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
    data = unicode(data, 'latin-1')
    self._tree = parseString(data.encode('ascii', 'xmlcharrefreplace'))
    self._movie = self._tree_to_movie(self._tree)
    
  def get_coqdoc_movie(self):
    return self._movie
