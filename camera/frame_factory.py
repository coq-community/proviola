from Frame import Frame
from coqdoc_frame import Coqdoc_Frame

class frame_maker(object):
  def __init__(self):
    self._constructors = {}

  def __call__(self, element):
    for name in self._constructors:
      if element.findAll(name = name):
        f =  self._constructors[name]()
        break
    else:
      f = Frame()

    f.fromxml(element)
    return f
  
  def register(self, name, constructor):
    self._constructors[name] = constructor

make_frame = frame_maker()
make_frame.register("command-coqdoc", Coqdoc_Frame)
