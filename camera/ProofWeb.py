# Author: Carst Tankink carst 'at' cs 'dot' ru 'dot' nl
# Copyright: Radboud University Nijmegen
#
# This file is part of the Proof Camera.
#
# Proof Camera is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Proof Camera is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Proof Camera.  If not, see <http://www.gnu.org/licenses/>.



"""ProofWeb class representing the abstract interface to ProofWeb.
"""

import urllib
import urllib2
import string 
import sys
import logging
from time import sleep

from ResultHandler import ResultHandler

class ProofWeb(object):
  def __init__(self, url, group = "nogroup", user = "nobody", 
                          pswd = "anon", prover="coq"):
    self.url = url
    self.session = -1
    self.pos = 0
    self.callnr = 1
    self.group = group
    self.user = user
    self.pswd = pswd
    self.prover = prover

    # Login to ProofWeb, get a session id.
    loginInfo = urllib.urlencode(
      {"login"  : "%s/%s"%(self.group, self.user),
       "pass"   : self.pswd,
       "prover" : self.prover
      })

    handler = ResultHandler()
    
    try:
      prover = urllib2.urlopen(self.url, loginInfo)
      data = prover.read()
      prover.close()
    
      # Parse the HTML, to get the variable assignments in the JavaScript
      handler.feed(data)
    
      #TODO Breaks if session is not found in the web page
      self.session = string.strip(handler.assignments['session'], '\"')
    except urllib2.HTTPError:
      print "Error sending login information"



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
        logging.debug("Error: %s"%result[1:])
        sys.exit()
        return ""
      else:
        # The goal has the form "+<goal description>__PWT__n__PWT__"
        end = string.find(result, "__PWT__")

        goal = result[1:end]
        return goal
    else:
      return ""

  
  def send(self, command):
    """ Send the given command to the prover, and give the goal returned by 
        ProofWeb.
    """  
    sleep(.5)

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
      logging.debug("Error sending command to ProofWeb")
      return ""

    goal = self.strip_decoration(prover.read())
    if goal == '<':
      return self.send(command)
    prover.close()

    self.pos = end
    self.callnr += 1
    return goal

