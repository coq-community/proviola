from xmlrpclib import ServerProxy

TIMEOUT = 60000
ARGS = []

class Isabelle_Session:

  def __init__(self, xmlRpcUrl, filename):
    self._isabelle = ServerProxy(xmlRpcUrl).Isabelle
    self._session_key = self._isabelle.start(TIMEOUT, ARGS, 
                        "/home/carst/Build/Isabelle2009-2", "")
    self._isabelle.begin_document(filename, self._session_key)
    
  def __del__(self):
    self._isabelle.stop(self._session_key)

  def add(self, contents):
    self._isabelle.add(contents, self._session_key)

  def document_as_xml(self):
    return self._isabelle.document_as_xml(self._session_key)
