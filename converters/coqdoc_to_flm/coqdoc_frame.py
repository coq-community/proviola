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

  def toxml(self, doc):
    """ Conver this frame to XML. """
    frame_xml = Frame.toxml(self, doc)
    
    frame_xml.appendChild(self.createTextElement(doc, TAG_COQDOC, 
                                                 self._command_coqdoc))
    
    return frame_xml

  def _create_html_element(self, doc, name, contents):
    """ Create an element whose children can be HTML markup. """
    
    
    return element 