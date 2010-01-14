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
    
    if char == None:
      return acc
    
    acc = acc + char
    
    if char == "*":
      char2 = self.readChar()
      acc = acc + char2
      if char2 == ")":
        open = open - 1
        if open == 0:
          return acc
        else:
          return self.getComment(acc, open)
      else:
        return self.getComment(acc, open)
    elif char == "(":
      char2 = self.readChar()
      acc = acc + char2
      if char2 == "*":
        return self.getComment(acc, open + 1)
      else:
        return self.getComment(acc, open)
    else:
      return self.getComment(acc, open)
  
  def getWord(self, acc, open = 0):
    char = self.readChar()
    
    if char == None:
      return acc
    
    acc = acc + char
    
    if char == "(":
      char2 = self.readChar()
      acc = acc + char2
      if char2 == "*":
        return self.getWord(acc, open + 1)
      else:
        return self.getWord(acc, open)
    elif char == "*":
      char2 = self.readChar()
      acc = acc + char2
      if char2 == ")":
        return self.getWord(acc, open - 1)
      elif char2 == ".":
        if open == 0: 
          return acc
      else:
        return self.getWord(acc, open)
    elif char == ".":
      nextChar = self.peekChar()
      if nextChar != ".":
        if open == 0:
          return acc
        else:
          return self.getWord(acc, open)  
      else:
        acc += self.readChar()
        return self.getWord(acc, open)
    else:
      return self.getWord(acc, open)
      
      
  def getCommand(self, acc = ""):
    char = self.readChar()
    
    if char == None:
      return acc
    
    acc = acc + char
    
    if char in string.whitespace:
      return self.getCommand(acc)
    elif char == "(":
      char2 = self.readChar()
      acc = acc + char2
      if char2 == "*":
        return self.getComment(acc)
      else:
        return self.getWord(acc)
    else: 
      return self.getWord(acc)
    
  def makeFrames(self, document, pw, remaining = ""):
    command = self.getCommand()
    print "Command: " + command
    if len(command) == 0:
      return
    
    if self.isComment(command):
      response = ""
    else:
      response = pw.send(command)
      print "Response: " + response
  
    document.addFrame(command, response) 
    self.makeFrames(document, pw)

  def isComment(self, text):
    return text.split()[0].startswith("(*") and text.endswith("*)")
