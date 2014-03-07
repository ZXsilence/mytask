#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wulingping
@contact: wulingping@maimiaotech.com
@date: 2014-01-23 15:29
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import os
import sys
from apicenter import ApiCenter
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

class ApiCenterClient(object):

    def __init__(self,host,port):
        self.host = host
        self.port = int(port)
        transport = TSocket.TSocket(self.host, self.port)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = ApiCenter.Client(protocol)
        transport.open()

    def execute(self,params,nick,soft_code,api_source):
        print nick,type(nick)
        #nick = nick.encode('utf8')
        return self.client.execute(params,nick.encode('utf8'),soft_code,api_source) 


