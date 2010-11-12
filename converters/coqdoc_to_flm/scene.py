class Scene(object):
  def __init__(self, id = 0):
    self.id = id
    self.frames = []

  def add_frame(self, frame):
    self.frames.append(frame)

