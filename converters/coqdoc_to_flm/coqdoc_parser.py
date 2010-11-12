""" A parser for Coqdoc's HTML. """
import xml.parsers.expat

import CoqReader
import coqdoc_movie
from Prover import get_prover
from scene import Scene
from coqdoc_frame import Coqdoc_Frame

class Coqdoc_Parser(object):
  def __init__(self):
    """ Initialize the parser-wrapper. """
    self._in_code = False
    self._reader = CoqReader.CoqReader()
    self._prover = get_prover(
                    "http://hair-dryer.cs.ru.nl/proofweb/index.html",
                    group = "nogroup")
    
    self._parser = self._setup_parser()
    self._movie = coqdoc_movie.Coqdoc_Movie()

    self._handling = None
    
    self._open_divs = 0
    self._code_depth = -1
    self._doc_depth = -1
    self._current_scene = None
    self._current_coqdoc = ""

  def _setup_parser(self):
    """ Setup an Expat parser for this class. """
    parser = xml.parsers.expat.ParserCreate()
    parser.StartElementHandler = self._start_handler
    parser.EndElementHandler = self._end_handler
    parser.CharacterDataHandler = self._char_data
    return parser

  def _start_handler(self, name, attrs):
    """ We are interested in:
      - divs: to determine a new scene.
      - title: to be able to set movie's title.
      - spans: because they tell us if particular frames should be hidden.
      - body: we are not interested in anything (except the title) 
              outside the body.
    """
    if self._open_divs > 0:
      self._current_coqdoc += "<{name}".format(name = name)
      for attr in attrs:
        self._current_coqdoc += ' {attr}="{value}"'.\
                format(attr = attr, value = attrs[attr])

      self._current_coqdoc += ">"

    if name == "span":
      self._handle_span(attrs)
    elif name == "div":
      self._handle_div(attrs)
    elif name == "title":
      self._handling = name
    else:
      self._handle_other(name, attrs)

  def _is_hidden(self, attrs):
    """ Test if the attributes contains a display: none style. """
    try:
      fstyle = attrs["style"]
      return style.find("display: none") != -1

    except KeyError:
      return False

  def _handle_other(self, name, attrs):
    """ Handle others, move them into the current pretty command.
    """
    if self._open_divs > 0:
      self._current_coqdoc += "<{name}>".format(name = name)

  def _handle_span(self, attrs):
    """ If the span contains the style="display:none" attribute, 
        mark this for the rest.
        We also keep track of how many spans are open.
    """
    pass 

  def _is_code_div(self, attrs):
    """ Return if the div being inspected is a code div. """
    try:
      return attrs["class"] == "code"
    except KeyError:
      return False

  def _is_doc_div(self, attrs):
    """ Return if the div being inspected is a code div. """
    try:
      return attrs["class"] == "doc"
    except KeyError:
      return False

  def _handle_div(self, attrs):
    """ Handle different types of divs:
      - divs of the code class: send the code to coq, partition into frames.
      - other divs: copied verbatim. 
    """
    self._open_divs += 1

    if self._is_code_div(attrs): 
      self._handling = "code"
      self._code_depth = self._open_divs
      self._current_scene = Scene()
    if self._is_doc_div(attrs):
      self._handling = "doc"
      self._doc_depth = self._open_divs
      self._current_scene = Scene()



  def _end_handler(self, name):
    if name == "title" and self._handling == "title":
      self._handling = None

    elif name == "div":
      if self._handling == "code" and self._open_divs == self._code_depth:
        # We have closed the code div
        self._handling = None
      elif self._handling == "doc" and self._open_divs == self._doc_depth:
        print("Doc: Current coqdoc: {pretty}".format(pretty = self._current_coqdoc))
        
        self._current_coqdoc = ""
        self._handling = None

      self._open_divs -= 1
    else:
      if self._open_divs > 0:
        self._current_coqdoc += "</{name}>".format(name = name)

  def _char_data(self, data):
    """ Character data is:
        - Copied over to the Coqdoc nodes if it occurs under a div. 
          - If it occurs under a code div, it is also sent to the prover.
        - If it occurs under a 
    """
    if self._open_divs > 0:
      self._current_coqdoc += data

    if self._handling == "title":
      self._movie.add_to_title(data)

    elif self._handling == "code":
      commands = self._reader.parse(data)
      if len(commands) == 1 and self._reader.isCommand(commands[0]):
        response = self._prover.send(commands[0])
        print("\n\nOne command: %s"%commands[0])
        print("Response: %s"%response)
        print("Current-coqdoc: {pretty}".format(pretty = self._current_coqdoc))
        frame = Coqdoc_Frame(command = commands[0], response = response, 
                             command_cd = self._current_coqdoc)
        self._current_scene.add_frame(frame)
        self._movie.addFrame(frame)
        self._current_coqdoc = ""

      elif len(commands) > 1:
        print("Commands: {cmds}".format(cmds = `commands`))

  def feed(self, data):
    """ 
    Feed data to the parser

    Arguments:
    - data: An string describing the XML tree to parse.
    
    Effect: self._coqdoc_movie is updated with the contents of data. 
    """
    self._parser.Parse(data)

  def get_coqdoc_movie(self):
    return self._movie
