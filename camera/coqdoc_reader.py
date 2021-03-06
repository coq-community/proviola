""" Implements a Reader class for Coqdoc documents. """
from xml.sax.saxutils import unescape
import copy
import re

from CoqReader import CoqReader
from Movie import Movie
from scene import Scene
from coqdoc_frame import Coqdoc_Frame

from StringIO import StringIO
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
#    code = unicode(code, encoding='utf-8')
    self._coqdoc_tree = html.parse(StringIO(code))

  def _get_text(self, div):
    """ Get the text embedded in div, replacing break tags with newlines. """
    try:
      if div.tag == 'br':
        if div.tail:
          tail = html.tostring(div, method='text', encoding='utf-8')
        else:
          tail = ""
        return '\n' + tail

      div_cp = copy.copy(div)
      for br in div_cp.findall(".//br"):
        prev = br.getprevious()
        if prev is not None:
          prev.tail = (prev.tail or '') + "\n"
        else:
          br.getparent().text = (br.getparent().text or '') + "\n" + (br.tail or '')

        br.getparent().remove(br)
      return html.tostring(div_cp, method='text', encoding="utf-8")

    except AttributeError, TypeError:
      return div
  
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
    result_scene = Scene()
    result_scene.set_type("code")
    result_scene.set_lang("coq")
    
    markup = []
    frame = None
    
    for child in [div.text or ''] + list(div):
      try:
        child_class = child.get('class')
      except AttributeError:
        child_class = '' 
      
      if child_class == "proof":
        subscene = self._process_code(child)
        result_scene.add_scene(subscene)

      else:
        markup.append(child)
        t = self._get_text(child)
        commands = self.parse(t)

        if commands and self.isCommand(commands[0]):
          command = self._replace_html(commands[0])
          if type(command) == type(u""):
            command = command.replace(u"\xa0", " ")
          else:
            command = command.decode("utf-8").replace(u"\xa0", " ")
            command = command.encode("utf-8")

          response = self._prover.send(command)
          frame = Coqdoc_Frame(command = command, command_cd = markup, response = response)
          frame.set_code(True)

          frame.set_dependencies(self._deps)
          self._deps = [frame]

          result_scene.add_scene(frame)

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
    trailing_frame.set_dependencies(self._deps)
    self._deps = [trailing_frame]
    result_scene.add_scene(trailing_frame)
    return result_scene
  
  def _process_doc(self, div):
    scene = Scene()
    scene.set_type("doc")
    scene.set_lang("coq")
    scene.set_attributes(div.items())
    
    if div.text is not None:
      child_scene = Coqdoc_Frame(command = div.text, command_cd = [div.text],
                                 response = None)
      scene.add_scene(child_scene)

    for child in div:
      tail_frame = None

      try:
        child_name = child.tag
      except AttributeError:
        child_name = "text"
        child.text = str(child)

      if child.tag == 'div':
        if div.get("class") == "doc":
          child_scene = self._process_doc(child)
        else:
          child_scene = self._process_div(child)

        if child.tail is not None:
          tail_frame = Coqdoc_Frame(command=child.tail, response=None,
                                    command_cd=[child.tail])

      else:
        # Common markup
        child_scene = Coqdoc_Frame(command = html.tostring(child, method='text',
                                                          encoding="utf-8"),
                             command_cd = [child], response = None)


      scene.add_scene(child_scene)

      if tail_frame:
        scene.add_scene(tail_frame)

    return scene
  
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
    title_el = self._coqdoc_tree.find(".//head/title")
    title = title_el.text if  title_el is not None else ""
    self._movie.set_title(title)
    
    body = self._coqdoc_tree.find(".//body")
    
    if body is not None:
      for div in body.findall("./div"):
        scene = self._process_div(div)
        self._movie.add_scene(scene)
        
    return self._movie
