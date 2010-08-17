# Author: Carst Tankink carst 'at' cs 'dot' ru 'dot' nl
# Copyright: Radboud University Nijmegen
#
# This file is part of the Coqdoc Pretty Printer.
#
# Coqdoc Pretty Printer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Coqdoc Pretty Printer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Coqdoc Pretty Printer.  If not, see <http://www.gnu.org/licenses/>.


import subprocess
from os import remove

class CoqDocDriver:
  ''' A driver for the coqdoc program '''

  def __init__(self):
    ''' Constructor for the driver

    This function opens a temporary file for communicating with coqdoc, 
    locates the CoqDoc executable and sets a dictionary of arguments (defaults
    based on the use in ppcoqdoc
    '''

    self._executable = '/usr/local/bin/coqdoc'
    self._filename = '/tmp/coqdoc-comm.v'
    self._args = { 'output'    : '--html',\
                   'redirect'  : '--stdout',\
                   'verbosity' : '--body-only',\
                   'index'     : '--no-index',\
                   'title'     : '--short', \
                   #'comments'  : '--parse-comments',\
                   }
    self._file = open(self._filename, 'w')

  def process(self, command):
    ''' Process a command through coqdoc, returning the pretty result.
    
    Precondition: 
    - self._file is opened for writing.

    Arguments:
    - command: the command that needs to be processed by CoqDoc.

    Returns:
    - The pretty-printed command, as returned by CoqDoc.

    Postcondition: 
    - self._file is opened for writing
    '''

    self._file.write(command)
    self._file.close()
   
    args = [self._executable] + list(self._args.values()) + [self._filename]
    coqdoc = subprocess.Popen(args, stdout=subprocess.PIPE,\
                              stderr=subprocess.PIPE)
    response = coqdoc.communicate()[0]
    self._file = open(self._filename, 'w')
    
    return response

  def __del__(self):
    ''' Destructor. Cleans up the temporary file we have created previously.
    '''
    
    self._file.close()
    remove(self._filename)
