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



import re
from HTMLParser import HTMLParser


""" Handle the HTML coming from ProofWeb.
"""
class ResultHandler(HTMLParser):
  def __init__(self):
    # Initialize the parent class
    HTMLParser.__init__(self)
    # The tag we are handling.
    self.handlingTag = "" 

    # A dictionary of variable, value assignments in the JavaScript of the
    # page
    self.assignments = {}

  def handle_starttag(self, tag, attr):
    self.handlingTag = tag

  def handle_endtag(self, tag):
    self.handlingTag = ""

  def handle_data(self, data):
    if self.handlingTag == "script" and len(data) > 0:
      exp = re.compile( r"\b\w*=\"\w*\"" )

      result = exp.findall(data)
      
      if result:
        for item in result:
          assignment = item.split("=")
          self.assignments[assignment[0]] = assignment[1]
    
