from Film import FilmDocument

class Reader:
  def __init__(self):
    self.script = ""
    self.line = ""

  def getLine(self):
    if self.line == "":
      self.line = self.getNextLine()

  def appendData(self, pw, data):
    document = FilmDocument()
    self.script += data
    self.makeFrames(document, pw)
    return document.toxml()
    
  def findNewLine(self):
    if self.script == None:
      return -1
    
    return self.script.find("\n")

  def read(self, filename):
    file = open(filename, 'r')
    self.script = file.read()
    file.close()
    
  def getNextLine(self):  
    if self.findNewLine() >= 0:
      result = self.script[0:self.findNewLine() + 1]
      self.script =  self.script[self.findNewLine() + 1 :]
      
    else:
      result = self.script
      self.script = "" 
    return result  
    
  def readChar(self):
    self.getLine()
    if len(self.line) == 0:
      return None
    
    char = self.line[0]
    self.line = self.line[1:]
    return char
  
  def peekChar(self):
    self.getLine()
    if len(self.line) > 0:
      return self.line[0]
    else:
      return ' '
    
      
import CoqReader
def getReader(filename):
  coqSuffix = CoqReader.suffix
  
  if filename.endswith(coqSuffix):
    return CoqReader.CoqReader(filename)

