#/usr/bin/python
from xml.dom.minidom import parse, parseString
import sys

openComment = "(*"
closeComment = "*)"

def getText(nodeList):
  result = ""
  for node in nodeList:
    if node.nodeType == node.TEXT_NODE:
      result += node.data

  return result

def hasComments(text):
  return openComment in text

def beginsWithComment(text):
  return text.find(openComment) == 0

def unbalanced(text):
  return text.count(openComment) > text.count(closeComment) 

def createPart(data, classType, doc):
  element = doc.createElement("part")
  element.setAttribute("class", classType)
  textData = doc.createTextNode(data)
  element.appendChild(textData)
  return element

def createCommentNode(text, doc):
  return createPart(text, "comment", doc)

def createLabelNode(text, doc):
  return createPart(text, "label", doc)

def createLemmaNode(text, doc):
  return createPart(text, "lemma", doc)

def createTextNode(text, doc):
  return createPart(text, "plain", doc)

def createObligationNode(text, doc):
  return createPart(text, "obligation", doc)

def replaceComments(element, doc, height = 0):
  text = getText(element.childNodes)
  result = []
  while len(text) > 0:
    if beginsWithComment(text):
      closeCmtPos = text.find(closeComment)
      
      while unbalanced(text[:closeCmtPos + len(closeComment)]):
        closeCmtPos +=  text[closeCmtPos + len(closeComment):].find(closeComment) + len(closeComment) 

      result += [createCommentNode(text[:closeCmtPos + len(closeComment)],doc)]
      text = text[closeCmtPos + len(closeComment):] 
    elif hasComments(text):
      openCmtPos = text.find(openComment)
      result += [createTextNode(text[:openCmtPos], doc)]
      text = text[openCmtPos:]
    else:
      result += [createTextNode(text, doc)]
      text = ""

  for child in element.childNodes:
    element.removeChild(child)
    child.unlink()
  
  for re in result:
    element.appendChild(re)

def matchKeywords(text, keywords):
  for kw in keywords:
    if text.find(kw) >= 0:
      return kw
  kw = None

def getLabel(nodes, keywords):
  startNode = None
  label = ""
  for node in nodes:
    if node.getAttribute("class") != "comment":
      txt = node.firstChild.data
      kw = matchKeywords(txt, keywords)
      if kw != None:
        startNode = node
        # Well-formed Coq texts should not break on this.
        label = txt.split()[1]
        if label.endswith(":"):
          label = label[:-1]
        break
  else:
    return (None, None)

  return (label, startNode)
  
def replaceLabels(element, document):
  keywords = ["Definition", "Fixpoint", "Inductive", "Lemma", "Theorem",\
              "Scheme", "Section", "End", "Ltac", "Example"]
  nodes = element.childNodes
  (label, node) = getLabel(nodes, keywords)
  if label != None:
    text = node.firstChild.data
    labelPos = text.find(label)
    beforeLabel = createTextNode(text[:labelPos], document)
    labelNode = createLabelNode(label, document)
    afterLabel = createTextNode(text[labelPos + len(label):], document)
    element.replaceChild(afterLabel, node)
    element.insertBefore(labelNode, afterLabel)
    element.insertBefore(beforeLabel, labelNode)

def findLemma(nodes):
  keywords = ["Example", "Lemma", "Theorem"]
  startNode = None
  endNode = None

  for node in nodes:
    text = node.firstChild.data
    for kw in keywords:
      if node.getAttribute("class") != "comment" and kw in text:
        if node.nextSibling.getAttribute("class") == "label":
          startNode = node.nextSibling.nextSibling
        else:
          print "No label, odd."

  if startNode != None: 
    endNode = startNode
    text = endNode.firstChild.data

    while text.find(".") < 0:
      endNode = endNode.nextSibling
      while endNode.getAttribute("class") == "comment":
        endNode = endNode.nextSibling
      if endNode == None:
        break
      text = endNode.firstChild.data

    return (startNode, endNode, text.find("."))

  return (None, None, -1)

def replaceLemma(element, document):
  nodes = element.childNodes
  (startNode, endNode, endPos) = findLemma(nodes)
  
  if startNode == None:
    return
  
  text = startNode.firstChild.data
  beforeNode = createTextNode(text[:text.find(":") + 1],document)

  if startNode == endNode:
    lemmaNode = createLemmaNode(text[text.find(":") + 1:endPos + 1], document)
    afterNode = createTextNode(text[endPos + 1:], document)
  else:
    lemmaNode = createLemmaNode(text[text.find(":") + 1:], document)
    node = startNode.nextSibling
    element.removeChild(startNode)
    startNode.unlink()
    while node != endNode:
      if node.getAttribute("class") == "comment":
        newNode = node.cloneNode(deep = True)
      else:
        newNode = document.createTextNode(node.firstChild.data)
      
      lemmaNode.appendChild(newNode)

      nxtNode = node.nextSibling
      element.removeChild(node)
      node.unlink()
      node = nxtNode
    # node == endNode
    text = endNode.firstChild.data
    lemmaNode.appendChild(document.createTextNode(text[:endPos + 1]))
    afterNode = createTextNode(text[endPos + 1:], document)
     
  element.replaceChild(afterNode, endNode)
  element.insertBefore(lemmaNode, afterNode)
  element.insertBefore(beforeNode, lemmaNode)

def prettyCommand(prettyElement, document):
  replaceComments(prettyElement, document)
  replaceLabels(prettyElement, document)
  replaceLemma(prettyElement, document)

def handleCommands(document, commands):
  for command in commands:
    commandPP = command.cloneNode(deep = True)
    prevPP = command.parentNode.getElementsByTagName("command-pp")
    if len(prevPP) > 0:
      command.parentNode.replaceChild( commandPP, prevPP[0])
    
    commandPP.tagName = "command-pp"
    prettyCommand(commandPP, document)
    command.parentNode.appendChild(commandPP)

def replaceObligations(element, document):
  if element.hasChildNodes():
    text = element.firstChild.data
    separator = "============================"
    if text.find(separator) >= 0:
      context = text[:text.find(separator) + len(separator)]
      obligation = text[text.find(separator) + len(separator):]
    else:
      context = text
      obligation = ""

    contextNode = createTextNode(context, document)
    obligationNode = createObligationNode(obligation, document)
    element.replaceChild(obligationNode, element.firstChild)
    element.insertBefore(contextNode, obligationNode)
      
def prettyResponse(responseElement, document):
  replaceObligations(responseElement, document)

def handleResponses(document, responses):
  for response in responses:
    responsePP = response.cloneNode(deep = True)
    prevPP = response.parentNode.getElementsByTagName("response-pp")
    if len(prevPP) > 0:
      response.parentNode.replaceChild( responsePP, prevPP[0])
    responsePP.tagName = "response-pp"
    prettyResponse(responsePP, document)
    response.parentNode.appendChild(responsePP)

def main(argv = None):
  if argv is None:
    argv = sys.argv
  if len(argv) > 1:
    film = argv[1]
    print "Processing:", film
  else:
    print "Too few arguments"
    return 2

  original = parse(film)
  styleSheetRef = original.createProcessingInstruction("xml-stylesheet",\
                          "type=\"text/xsl\" href=\"proviola-pp.xsl\"")  
  original.insertBefore(styleSheetRef, original.documentElement)
  commands = original.getElementsByTagName("command")
  handleCommands(original, commands)
  responses = original.getElementsByTagName("response")
  handleResponses(original, responses)
  
  if len(argv) > 2:
    newFile = argv[2]
  else:
    newFile = film
  target =  open(newFile, 'w')
  original.writexml(target)

if __name__ == "__main__":
  sys.exit(main())
