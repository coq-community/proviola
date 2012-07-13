""" Implements a Reader class for Coqdoc documents. """
from xml.sax.saxutils import unescape
import copy
import re

from CoqReader import CoqReader
from Movie import Movie
from scene import Scene
from coqdoc_frame import Coqdoc_Frame

from cStringIO import StringIO
from lxml import html

suffix = ".html"

class Coqdoc_Reader(CoqReader):
  """ Reader that reads Coqdoc-produces HTML files, creating a movie maintaining
      the original layout, with state output inlined.
  """
  
  def __init__(self):
    """ Setup: creates an empty movie. """
    CoqReader.__init__(self)
    self._movie = Movie()
    self._prover = None
    self._coqdoc_tree = None
   
  def add_code(self, code):
    """ Override of the corresponding method in Reader: makes a 
        lxml tree out of the given Coqdoc document. """
    self._coqdoc_tree = html.parse(StringIO(code))

  def _get_text(self, div):
    """ Get the text embedded in div, replacing break tags with newlines. """
    if div.tag == 'br':
      return '\n' + (div.tail or '')

    div_cp = copy.copy(div)
    for br in div_cp.findall(".//br"):
      prev = br.getprevious()
      if prev is not None:
        prev.tail = (prev.tail or '') + "\n"
      else:
        br.getparent().text = (br.getparent().text or '') + "\n" + (br.tail or '')

      br.getparent().remove(br)

    return html.tostring(div_cp, method='text',
                         encoding=self._coqdoc_tree.docinfo.encoding)

  
  def _replace_html(self, text):
    """ Replace HTML entitities by ASCII equivalents. 
        Special entities taken from SF's symbols.v """
    replacements = {"&nbsp;":   " ",
                    "&#160;":   " ", # Unicode nbsp; should be standard space for Coq
                    "&rarr;":   "->",
                    "&larr;":   "<-",
                    "&Gamma;":  "Gamma",
                    "&forall;": "forall",
                    "&exist;":  "exists",
                    "&exists;": "exists",
                    "&dArr;":   "||",
                    "&Arr;":    "==>",
                    "&harr;":   "<->",
                    "&and;":    "/\\",
                    "&or;":     "\/",
                    "&#8658;":   "~~>",
                    "&#8660;":   "<~~>",
                    "&#8866;":   "|-",
                    }

    text = unescape(text, replacements)
    return text
  
  def _process_code(self, div):
    """ Process a code div, returning a scene and the frames referenced.
    """
    frames = []
  
    scene = result_scene = Scene()
    result_scene.set_type("code")
    
    text = [div.text or '']
    markups = list(text)
     
    for child in div:
      if child.get("class") == "proof":
        scene = Scene()
        scene.set_type("code")
        result_scene.add_scene(scene)
        
        if child.text:
          text.append(child.text)
          markups.append(child.text)
  
        for grandchild in child:
          markups.append(grandchild)
          text.append(self._get_text(grandchild))

      else:
        markups.append(child)
        text.append(self._get_text(child))

    markup = []
    frame = None
    for mkup, code in zip(markups, text):
      markup.append(mkup)
      commands = self.parse(code)
      
      if commands and self.isCommand(commands[0]):
        command = self._replace_html(commands[0])
        response = self._prover.send(command)
        frame = Coqdoc_Frame(command = command, command_cd = markup, response = response)
        frame.set_code(True)
        frames.append(frame)
        scene.add_scene(frame)

        markup = []
        commands = []

      elif commands and commands[0] == '\n' and frame is not None:
        frame.set_command(frame.getCommand() + '\n')
        frame.append_to_markup(markup[0])
        markup = markup[1:]
    
    trailing_frame = Coqdoc_Frame(command = ''.join([el for el in commands]),
                                  command_cd = markup,
                                  response = None)
    trailing_frame.set_code(True)
    frames.append(trailing_frame)
    scene.add_scene(trailing_frame)
    return frames, result_scene
  
  def _process_doc(self, div):
    frames = []
    scene = Scene()
    scene.set_type("doc")
    scene.set_attributes(div.items())
    
    if div.text is not None:
      child_scene = Coqdoc_Frame(command = div.text, command_cd = [div.text],
                                 response = None)
      scene.add_scene(child_scene)
      frames.append(child_scene)

    for child in div:
      try:
        child_name = child.tag
      except AttributeError:
        child_name = "text"
        child.text = str(child)

      if child.tag == 'div':
        if div.get("class") == "doc":
          child_frames, child_scene = self._process_doc(child)
        else:
          child_frames, child_scene = self._process_div(child)
      else:
        # Common markup
        child_scene = Coqdoc_Frame(command = html.tostring(child, method='text'),
                             command_cd = [child], response = None)
        child_frames = [child_scene]



      frames += child_frames
      scene.add_scene(child_scene)

      if child.tail is not None:
        frame = Coqdoc_Frame(command = child.tail, command_cd = [child.tail],
                             response = None)
        frames.append(frame)
        scene.add_scene(frame)


          
    return frames, scene
  
  def _is_code(self, div):
    """ Test whether the given div is a code div. """
    return div.get("class") and "code" in div.get("class").split()

  def _process_div(self, div):
    """ Given a div element, return a list of frames with the div's content, 
        and a scene mimicking its structure.  """
    
    if self._is_code(div):
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
      self._movie.set_title(self._coqdoc_tree.find(".//head/title").text)
    except AttributeError:
      self._movie.set_title("")
    
    
    body = self._coqdoc_tree.find(".//body")
    
    if body is not None:
      for div in body.findall("./div"):
        (frames, scene) = self._process_div(div)
          
        for frame in frames:
          self._movie.addFrame(frame)
          
        self._movie.add_scene(scene)
        
    return self._movie
