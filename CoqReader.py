import re
import Reader
import string

suffix = '.v'

class CoqReader(Reader.Reader):
  def __init__(self, filename = ""):
    Reader.Reader.__init__(self)
    self.suffix = ".v"
    if filename != "":
      self.basename = filename[:-len(suffix)]
      self.read(filename)

  def coqUndot(self, scriptText):
    result = scriptText.replace("Undo.Undo", "Undo. ndo")
    result = result.replace("...", "__.") 
    result = result.replace("..", "__")
    result = re.sub(r'\.[a-zA-Z1-9_]', "AA", result)
    return result
  
  def getComment(self, acc, open = 1):
    char = self.readChar() 
    while char != None and open > 0:
      acc = acc + char
      if char == "*":
        char2 = self.peekChar()
        if char2 == ")":
          acc = acc + self.readChar()
          open -= 1
          if open == 0:
            break
      elif char == "(":
        char2 = self.peekChar()
        if char2 == "*":
          acc = acc + self.readChar()
          open += 1
      char = self.readChar() 
    return acc

  def terminator(self, char, open):
    if char == ".":
      return self.peekChar() in string.whitespace and open == 0

  def getWord(self, acc, open = 0):
    char = self.readChar()
    while char != None:
      acc = acc + char
      if self.terminator(char, open):
        break
      if char == "(":
        char2 = self.peekChar()
        if char2 == "*":
          acc = acc + self.readChar()
          open += 1
      elif char == "*":
        char2 = self.peekChar()
        if char2 == ")":
          acc = acc + self.readChar()
          open -= 1

      char = self.readChar()
    return acc
      
  def getCommand(self, acc = ""):
    char = self.readChar()
    while char != None:
      acc = acc + char
      if char == "(":
        char2 = self.peekChar()
        if char2 == "*":
          acc = acc + self.readChar()
          return self.getComment(acc)
        else:
          return self.getWord(acc)
      elif not(char in string.whitespace): 
        return self.getWord(acc)
      char = self.readChar()
      
    return acc

  def parse(self, buffer):
    self.script = buffer
    command = self.getCommand()
    result = []
    while (len(command) != 0):
      result.append(command)
      command = self.getCommand()
    return result
  
  def makeFrames(self, document, pw, remaining = ""):
    command = self.getCommand()
    while command != None and len(command) != 0:
      if self.isComment(command):
        response = ""
      else:
        response = pw.send(command)
      document.addFrame(command, response)  
      command = self.getCommand()
    
  def isComment(self, text):
    return len(text.split()) <= 0 or\
           text.split()[0].startswith("(*") and text.endswith("*)")
  
  def isCommand(self, text):
    return self.terminator(text[len(text) - 1], 0)
