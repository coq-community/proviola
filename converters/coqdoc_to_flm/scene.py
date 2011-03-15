from BeautifulSoup import Tag
from coqdoc_frame import Coqdoc_Frame

class Scene(object):
  def __init__(self, no = 0):
    self._no = no
    self._subscenes = []
    self._attributes = []
    self._type = None
  
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
    return self._attributes
  
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
  
  def toxml(self, document):
    """ Create an XML subtree out of this scene, as generated in document.
    """
    element = Tag(document, "scene")
        
    for key, value in self._attributes:
      element[key] = value
        

    element["scenenumber"] = self._no
    element["class"] = self._type

    for sub in self._subscenes:
      element.append(sub.get_reference(document))
    
    return element
 
  def fromxml(self, element):
    """ Unmarshall the scene from the given element.
    """
    self.set_attributes(element.attrs)

    try:
      self.set_type(element['class'])
    except KeyError:
      print "Class does not exist in element {el}, setting to doc.".\
          format(el = element)
      self.set_type("doc")

    self.set_number(['scenenumber'])

    for child in element.findAll(recursive = False):
      if child.name == "scene":
        sub_scene = Scene()
        sub_scene.fromxml(child)
      elif child.name == "frame-reference":
        sub_scene = Coqdoc_Frame(id = child["framenumber"])

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
  
  def get_reference(self, document):
    """ Returns a reference to this scene: for scenes, we inline its XML 
        rendering. """
    
    return self.toxml(document)
