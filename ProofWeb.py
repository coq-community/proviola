"""ProofWeb class representing the abstract interface to ProofWeb.
"""

import urllib
import urllib2
import string 
import sys

from ResultHandler import ResultHandler

class ProofWeb:
  def __init__(self, url):
    self.url = url
    self.session = -1
    self.pos = 0
    self.callnr = 1

    # Login to ProofWeb, get a session id.
    loginInfo = urllib.urlencode( \
      {"login"  : "nogroup/nobody", \
       "pass"   : "anon", \
       "prover" : "coq" \
      })

    handler = ResultHandler()

    prover = urllib2.urlopen(self.url, loginInfo)
    
    data = prover.read()
    prover.close()

    # Parse the HTML, to get the variable assignments in the JavaScript
    handler.feed(data)
    #TODO Breaks if session is not found in the web page
    self.session = string.strip(handler.assignments['session'], '\"')


  """Strip the ProofWeb decoration from the result, and return the undecorated goal.
     Returns the empty string if an error was encountered.
  """
  def strip_decoration(self, result):
    if result != "":
      status = result[0]

      # DONE: "<" signifies a rerequest.
      if status == '<':
        return status
      if status == '-' or status == "<":
        print "Error: %s"%result[1:]
        sys.exit()
        return ""
      else:
        # The goal has the form "+<goal description>__PWT__n__PWT__"
        end = string.find(result, "__PWT__")

        goal = result[1:end]
        return goal
    else:
      return ""

  """Send the given command to the prover, and give the goal returned by ProofWeb.
  """

  def send(self, command):
    cmdarg = "%d__PWT__%s__PWT__%d"
    begin = self.pos
    end = self.pos + len(command)
    cmdarg = cmdarg%(begin, command, end)
    
    commandInfo = urllib.urlencode( \
      { "command"      : "addtobuf", \
        "callnr"       : self.callnr, \
        "s"            : self.session, \
        "cmdarguments" : cmdarg \
      })
    
    try:
      prover = urllib2.urlopen(self.url, commandInfo)
    except urllib2.HTTPError:
      print "Error sending command to ProofWeb"
      return ""

    
    goal = self.strip_decoration(prover.read())
    if goal == '<':
      return self.send(command)
    prover.close()

    self.pos = end
    self.callnr += 1
    return goal

