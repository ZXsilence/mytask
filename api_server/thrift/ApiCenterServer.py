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

def useage():
    print 'python ApiCenterServer \n python ApiCenterServer ip port'
   
if __name__ == '__main__':
    if len(sys.argv) == 1:
        ip = API_THRIFT['host']
        port = API_THRIFT['port']
    elif len(sys.argv) == 3:
        ip = sys.argv[1]
        port = sys.argv[2]
    else:
        useage()
        sys.exit(0)
    handler = ApiCenterHandle()
    processor = ApiCenter.Processor(handler)
    transport = TSocket.TServerSocket(ip, port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TForkingServer(processor, transport, tfactory, pfactory)
    print 'bind_ip:',ip,' port:',port
    print "Start api thrift server successfully ..."
    server.serve()


