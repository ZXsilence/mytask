#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2014-01-23 15:21
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import os
import sys
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
    from api_server.conf.set_env import getEnvReady
    getEnvReady()
from apicenter import ApiCenter
from apicenter.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from api_server.conf.settings import API_THRIFT
from api_server.thrift.ApiCenterHandle import ApiCenterHandle
   
if __name__ == '__main__':
    handler = ApiCenterHandle()
    processor = ApiCenter.Processor(handler)
    transport = TSocket.TServerSocket(API_THRIFT['host'], API_THRIFT['port'])
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print "Starting api thrift server ..."
    server.serve()


