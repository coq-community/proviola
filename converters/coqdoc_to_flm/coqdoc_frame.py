from Frame import Frame
from BeautifulSoup import Tag
TAG_COQDOC = "command-coqdoc"


class Coqdoc_Frame(Frame):
  """ A coqdoc_frame is a frame with an added command-coqdoc section. """
  def __init__(self, id = -1, command = None, 
                             command_cd = None, 
                             response = None):
    Frame.__init__(self, id = id, command = command, response = response)
    self._command_coqdoc = command_cd

  def set_number(self, number):
    """ Frames should not keep a scene-number. """
    pass
  
  def get_coqdoc_command(self):
    """ Getter for self._command_coqdoc. """
    return self._command_coqdoc
  
    
  def is_scene(self):
    return False

  def fromxml(self, element):
    """ Instantiate the data using the given element.
    """ 
    Frame.fromxml(self, element)
    self._command_coqdoc = element.find(TAG_COQDOC)
      
  def toxml(self, doc):
    """ Convert this frame to XML. """
    frame_xml = Frame.toxml(self, doc)
    tag = Tag(doc, TAG_COQDOC)
    
    for child in self._command_coqdoc:
      tag.append(child)
      
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
