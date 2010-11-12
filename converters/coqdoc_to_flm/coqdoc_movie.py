from Movie import Movie

from coqdoc_frame import Coqdoc_Frame

class Coqdoc_Movie(Movie):
  """ A coqdoc movie is a movie enhanced with scenes. """
  
  def __init__(self):
    """ Initialize an empty Movie. """
    Movie.__init__(self)

    self._title = ""
    self._scenes = []

  def add_scene(self, scene):
    self._scenes.append(scene)

  def add_to_title(self, title):
    self._title += title
