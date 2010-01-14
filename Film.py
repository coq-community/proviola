from xml.dom.minidom import Document

class FilmDocument(Document):
  def __init__(self):
    Document.__init__(self)
    self.frameNumber = 0
    self.film = self.createElement("film")

    movie = self.createElement("movie")
    self.appendChild(movie)
    movie.appendChild(self.film)

  def constructFrame(self, command, response):
    frame = self.createElement("frame")
    frame.setAttribute("frameNumber", "%s"%self.frameNumber)
    frame.appendChild(self.createTextElement("command", command))  
    frame.appendChild(self.createTextElement("response", response)) 
    return frame

  def createTextElement(self, elementName, contents):
    element = self.createElement(elementName)
    text = self.createTextNode(contents)
    element.appendChild(text)
    return element 

  def addFrame(self, command, response):
    frame = self.constructFrame(command, response)
    self.film.appendChild(frame)
    self.frameNumber += 1


  def writeFilm(self, fileName):
    filmFile = open(fileName, 'w')
    filmFile.write(self.toxml())
    filmFile.close()

 
  
