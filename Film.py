from xml.dom.minidom import Document

class FilmDocument(Document):
  def __init__(self, styleSheetUrl="\"moviola.xsl" + "\""):
    Document.__init__(self)
    self.frameNumber = 0
    self.film = self.createElement("film")
    
    styleSheetRef = self.createProcessingInstruction("xml-stylesheet",\
                                                     "type=\"text/xsl\" href=" + styleSheetUrl)
    
    self.appendChild(styleSheetRef)
    
    movie = self.createElement("movie")
    self.appendChild(movie)
    movie.appendChild(self.film)

  def constructFrame(self, command, response, tagname = "frame"):
    frame = self.createElement(tagname)
    frame.setAttribute("frameNumber", "%s"%self.frameNumber)
    frame.appendChild(self.createTextElement("command", command))  
    frame.appendChild(self.createTextElement("response", response)) 
    return frame

  def constructRawFrame(self, command, response):
    return self.constructFrame(command, response, "rawFrame")
   
  def createTextElement(self, elementName, contents):
    element = self.createElement(elementName)
    text = self.createTextNode(contents)
    element.appendChild(text)
    return element 

  def addFrame(self, command, response):
    frame = self.constructFrame(command, response)
    self.film.appendChild(frame)
    self.frameNumber += 1
  
  def addRawFrame(self, command, response):
    frame = self.constructRawFrame(command, response)
    self.film.appendChild(frame)
    self.frameNumber += 1

  def writeFilm(self, fileName):
    filmFile = open(fileName, 'w')

    filmFile.write(self.toxml())
    filmFile.close()

  def tolist(self):
    result = []
    
    for frame in self.film.childNodes:
      result.append(frame.toxml())
    
    return result
 
  
