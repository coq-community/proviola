import os
import time
from xml.dom.minidom import parseString, Node

from Reader import Reader
from Isabelle_Session import Isabelle_Session
from Frame import Frame
from Movie import Movie

suffix = '.thy'

class Isabelle_Reader(Reader):
  def make_frames(self, service_uri = "http://localhost:8080/xmlrpc/xmlrpc",
                        filename = "",
                        *args):
    document = Movie()
    isabelle_session = Isabelle_Session(service_uri, filename)
    contents = self.script
    isabelle_session.add(contents)
    #TODO: Poll for change (or comet-push on change?)
    time.sleep(10)
    tree = parseString("<document>" + isabelle_session.document_as_xml() +
                       "</document>")
    
    for node in tree.documentElement.childNodes:
      if node.nodeType != Node.TEXT_NODE and node.tagName == "state":
        document.addFrame(self.state_to_frame(node))
    return document

  def state_to_frame(self, state):
    id = 0
    command = self.command_from_state(state)
    response = self.response_from_state(state)
    return Frame(id, command,response)

  def command_from_state(self, state):
    """ Traverse the state tree, returning the contents of the source node in
      command.
    """
    try:
      command = state.getElementsByTagName("command")[0]
      source = command.getElementsByTagName("source")[0]
    except IndexError:
      return ""

    return source.firstChild.data

  def response_from_state(self, state):
    """ Traverse the state tree, returning the contents of the results node as
        an HTML pre containing HTML spans.
    """
    result = ""

    try:
      results = state.getElementsByTagName("results")[0]

      for pre in results.childNodes:
        assert pre is not None and pre.tagName == "pre"
        self.filter_non_spans(pre)

        result += pre.toxml()

    except (IndexError, AssertionError):
      return None

    return result
      
  def filter_non_spans(self, node):
    """ Recursively filter out the non-spans below the current node.
    """
    for child in node.childNodes:
      if child.nodeType != Node.TEXT_NODE and child.tagName == "data":
        data = child

        to_remove = []
        
        for child in data.childNodes:
          if child.tagName == "span":
            self.filter_non_spans(child)
          else:
            to_remove.append(child)

        for candidate in to_remove:
          data.removeChild(candidate)
        
        # Only good nodes are left now, so gather these nodes to live with 
        # their grandparent
        for child in data.childNodes:
          node.insertBefore(child, data)

        # Kill off the data span
        node.removeChild(data)
        data.unlink()
