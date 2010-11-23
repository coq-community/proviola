from Frame import Frame
from xml.dom.minidom import parseString
TAG_COQDOC = "command-coqdoc"

class Coqdoc_Frame(Frame):
  """ A coqdoc_frame is a frame with an added command-coqdoc section. """
  def __init__(self, id = 0, command = None, 
                             command_cd = None, 
                             response = None):
    Frame.__init__(self, id = id, command = command, response = response)
    self._command_coqdoc = command_cd

  def set_number(self, number):
    """ Frames should not keep a scene-number. """
    pass

  def toxml(self, doc):
    """ Convert this frame to XML. """
    frame_xml = Frame.toxml(self, doc)
    frame_xml.appendChild(parseString("<command-coqdoc>" + self._command_coqdoc.encode('ascii', 'xmlcharrefreplace') + "</command-coqdoc  >").documentElement)
    
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
  def _create_html_element(self, doc, name, contents):
    """ Create an element whose children can be HTML markup. """
    return element 
