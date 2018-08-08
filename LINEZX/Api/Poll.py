# -*- coding: utf-8 -*-
from thrift.transport import THttpClient
from thrift.protocol import TCompactProtocol
from .config import Config
from akad import TalkService
from akad.ttypes import *

class Poll(Config):

  client = None

  rev = 0

  def __init__(self, authToken):
    Config.__init__(self)
    self.transport = THttpClient.THttpClient(self.LINE_HOST_DOMAIN, None, self.LINE_API_QUERY_PATH_FIR)
    self.transport.path = self.LINE_AUTH_QUERY_PATH
    self.transport.setCustomHeaders({"X-Line-Application" : self.APP_NAME,"User-Agent" : self.USER_AGENT,"X-Line-Access": authToken})
    self.protocol = TCompactProtocol.TCompactProtocol(self.transport);
    self.client = TalkService.Client(self.protocol)
    self.rev = self.client.getLastOpRevision()
    self.transport.path = self.LINE_POLL_QUERY_PATH_FIR
    self.transport.open()

  def polling(self):    
    while True:
      Ops = self.client.fetchOperations(self.rev, 50)
      for Op in Ops:
        if (Op.type != OpType.END_OF_OPERATION):
          self.rev = max(self.rev, Op.revision)
          return Op
