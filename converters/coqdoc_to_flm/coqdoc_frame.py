from Frame import Frame
TAG_COQDOC = "command-coqdoc"

class Coqdoc_Frame(Frame):
  """ A coqdoc_frame is a frame with an added command-coqdoc section. """
  def __init__(self, id = 0, command = None, 
                             command_cd = None, 
                             response = None):
    Frame.__init__(self, id = id, command = command, response = response)
    self._command_coqdoc = command_cd

    
