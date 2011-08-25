from Frame import Frame
from coqdoc_frame import Coqdoc_Frame

def make_frame(element):
  """ Factory method creating a frame from XML element, filling it with
      the data in this element. """

  if element.findAll(name = "command-coqdoc"):
    f = Coqdoc_Frame()
  else:
    f = Frame()
  
  f.fromxml(element)
  return f
