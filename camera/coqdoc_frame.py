from Frame import Frame
from xml.sax.saxutils import escape, unescape
from external.BeautifulSoup import Tag
TAG_COQDOC = "command-coqdoc"


class Coqdoc_Frame(Frame):
  """ A coqdoc_frame is a frame with an added command-coqdoc section. """
  def __init__(self, id = -1, command = None, 
                             command_cd = None, 
                             response = None):
    Frame.__init__(self, id = id, command = command, response = response)
    self._command_coqdoc = command_cd or []

  def set_number(self, number):
    """ Frames should not keep a scene-number. """
    pass
  
  def get_coqdoc_command(self):
    """ Getter for self._command_coqdoc. """
    result = ""

    if not self._command_coqdoc:
      return result

    for part in self._command_coqdoc:
      result += str(part)

    return result
    
  def is_scene(self):
    return False

  def fromxml(self, element):
    """ Instantiate the data using the given element.
    """ 

    Frame.fromxml(self, element)
    self._command_coqdoc = [element.find(TAG_COQDOC)]
  
  def _escape(self, node):
    """ Escape entities in the node's text. """
    try:
      return escape(unescape(node))
    
    except TypeError:
      for child in node:
        child.replaceWith(self._escape(child))
              
    return node
        
    
  def toxml(self, doc):
    """ Convert this frame to XML. """
    frame_xml = Frame.toxml(self, doc)
    tag = Tag(doc, TAG_COQDOC)
    
    if self._command_coqdoc:
      for part in self._command_coqdoc: 
        tag.append(self._escape(part))
      
    frame_xml.append(tag)
    
    return frame_xml
  
  def __str__(self):
    return """
Frame(id       = {id},
      command  = {command},
      coqdoc   = {command_cd}
      response = {response})""".format(id = self._id, 
                                       command = self._command,
                                       command_cd = self._command_coqdoc,
                                       response = self._response)
