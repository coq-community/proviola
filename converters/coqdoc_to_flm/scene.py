from BeautifulSoup import Tag

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
    
  def add_scene(self, scene):
    """ Add a subscene to this scene.    
    Arguments:
      - scene: The subscene to be added. Can also be a Frame 
    Result: 
      - self.subscenes = self.subscenes' + [scene] 
    """
    
    scene.set_number(len(self._subscenes))
    self._subscenes.append(scene)
  
  def set_number(self, number):
    """ Set this scene's sceneNumber (self._no) """
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
        

    element["sceneNumber"] = self._no
    element["class"] = self._type

    for sub in self._subscenes:
      element.append(sub.get_reference(document))
    
    return element
  
  def __str__(self):
    result = "Scene(id = {id}".format(id = self._no)
    for scene in self._subscenes:
      result += ", sub_ref: {sub}".format(sub=scene.get_reference())
    result += ")"
    return result
  
  def get_reference(self, document):
    """ Returns a reference to this scene: for scenes, we inline its XML 
        rendering. """
    
    return self.toxml(document)
