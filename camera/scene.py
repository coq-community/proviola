from lxml import etree

from coqdoc_frame import Coqdoc_Frame

class Scene(object):
  def __init__(self, no = 0):
    self._no = no
    self._subscenes = []
    self._attributes = []
    self._type = None
    self.name = ""
    self.id = ""
    self.level = 0

  def set_attributes(self, attrs):
    """ Add a NamedNodeMap of attribute objects to this scene, which is exported
        verbatim to the XML rendering of the scene.
        
        Arguments:
        - attrs: The attributes to be added to the Scene.
    """
    self._attributes = attrs
  
  def is_scene(self):
    return True
  
  def get_attributes(self):
    """ Getter for self._attributes. """
    
    result_dict ={}
    for key, value in self._attributes:
      result_dict[key] = value
    return result_dict
  
  def remove_scenes(self):
    """ Remove all subscenes from this scene. """
    self._subscenes = []

  def add_scene(self, scene):
    """ Add a subscene to this scene.    
    Arguments:
      - scene: The subscene to be added. Can also be a Frame 
    Result: 
      - self.subscenes = self.subscenes' + [scene] 
    """
    scene.set_number(len(self._subscenes))
    self._subscenes.append(scene)

  def replace_frame(self, old_frame, new_frame):
    """ Replace old_frame with new_frame. """
    self._subscenes[self._subscenes.index(old_frame)] = new_frame

  def get_subscenes(self):
    """ Getter for self._subscenes. """
    return self._subscenes
  
  def flatten(self):
    """ Flatten all subscenes. """
    result = []
    for sub in self._subscenes:
      result += sub.flatten()
    return result

  def get_type(self):
    """ Getter for self._type. """
    return self._type
  
  def set_number(self, number):
    """ Set this scene's scenenumber (self._no) """
    self._no = number
    
  def set_type(self, type):
    """ Set this scene's type.
    
    Arguments:
     - type: A string, one of doc or code.
    """
    self._type = type
  
  def toxml(self):
    """ To XML, using lxml.etree. """
    element = etree.Element("scene")
    
    for key, value in self._attributes:
      element.set(key, value)

    element.set("scenenumber", str(self._no))
    element.set("class", self._type or "doc")
    element.set("level", str(self.level))
    element.set("name", self.name)
    element.set("identifier", self.id)
    
    for sub in self._subscenes:
      element.append(sub.get_reference())

    return element

  def fromxml(self, element):
    """ Unmarshall the scene from the given element.
    """
    self.set_attributes(element.items())

    try:
      self.set_type(element.get('class'))
    except KeyError:
      self.set_type("doc")

    self.set_number(element.get('scenenumber'))
    self.level = int(element.get('level'))
    self.name  = element.get('name')
    self.id = element.get('identifier')

    for child in element:
      if child.tag == "scene":
        sub_scene = Scene()
        sub_scene.fromxml(child)
      elif child.tag == "frame-reference":
        sub_scene = Coqdoc_Frame(id = child.get("framenumber"))

      self.add_scene(sub_scene)
  
  def getId(self):
    """ Getter for number. """
    return self._no
    
  def __str__(self):
    result = "Scene(id = {id}".format(id = self._no)
    for scene in self._subscenes:
      result += ", sub_ref: {sub}".format(sub=scene)
    result += ")"
    return result
  
  def get_reference(self):
    """ Return a reference to this scene. Subscenes are inlined for now. """
    return self.toxml()
