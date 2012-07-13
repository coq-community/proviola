from Frame import Frame
from functools import partial
from lxml import etree

TAG_COQDOC = "command-coqdoc"


class Coqdoc_Frame(Frame):
  """ A coqdoc_frame is a frame with an added command-coqdoc section. """
  def __init__(self, id = -1, command = None, 
                             command_cd = None, 
                             response = None):
    Frame.__init__(self, id = id, command = command, response = response)
    self._command_coqdoc = command_cd if command_cd is not None else []

  def get_coqdoc_command(self):
    """ Getter for self._command_coqdoc. """
    if not self._command_coqdoc:
      return ""
    
    return "".join([self._tostring(part) for part in self._command_coqdoc])

  def append_to_markup(self, element):
    """ Append element to markup. """
    self._command_coqdoc.append(element)

  def _tostring(self, el):
    """ Converts html.tostring(el) if el is an element, or el itself. """
    try:
      return etree.tostring(el)
    except TypeError:
      return el

  def get_markup_command(self):
    """ Getter for marked up command. """
    return self.get_coqdoc_command()

  def fromxml(self, element):
    """ Instantiate the data using the given element.
    """ 
    Frame.fromxml(self, element)    
    
    el = element.find(TAG_COQDOC)
    
    if el.text:
      self._command_coqdoc.append(el.text)
    
    map(self._command_coqdoc.append, el)

  
  def _append_etree(self, root, element):
    """ Append element to root. If element is text, it will overwrite root.text.
    """
    try:
      root.append(element)
    except TypeError:
      root.text = element

  def toxml(self):
    """ Convert this frame to XML, using etree. """
    frame_xml = Frame.toxml(self)
    coqdoc = etree.SubElement(frame_xml, TAG_COQDOC)
   
    map(partial(self._append_etree, coqdoc), self._command_coqdoc)
    
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
