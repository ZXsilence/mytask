#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import suds
import simplejson as json

'''
    webservice client
'''

import sys,os,re
from xml.sax import handler,parseString


class BaiduApiClient(object):
    
    token = "68999ddbadc5e6ca6d84e8094e2728e1"
    serverUrl = "https://api.baidu.com"

    def __init__(self, platform, service_name):
        self.client = None

        if platform == "sms":
            url = self.serverUrl + '/sem/sms/v3/' + service_name + '?wsdl'
        elif platform == "nms":
            url = self.serverUrl + '/sem/nms/v2/' + service_name + '?wsdl'
        else:
            return
            
        self.client = suds.client.Client(url)

    def set_authheader(self, username, access_token):
        self.header = self.client.factory.create('ns0:AuthHeader')
        self.header.username = username 
        self.header.token = self.token 
        self.header.accessToken = access_token 
        self.header.target = None 

        self.client.set_options(soapheaders=self.header)


def parse_suds_obj(suds_obj):
    dict = {}
    for e in suds_obj:
       if e.getText() != None:
           if dict.has_key(e.qname()):
               if type(dict[e.qname()]) != type([]):
                   dict[e.qname()] = [dict[e.qname()], e.getText()] 
               else:
                   dict[e.qname()].append(e.getText())
           else:
               dict[e.qname()] = e.getText()
       else:
           t = parse_suds_obj(e)
           if dict.has_key(e.qname()):
               if type(dict[e.qname()]) != type([]):
                   dict[e.qname()] = [dict[e.qname()], t] 
               else:
                   dict[e.qname()].append(t)
           else:
               dict[e.qname()] = t 
    return dict 
    

def parse_soap_response(res):
    resheader = res.getChild("Envelope").getChild("Header").getChild("ResHeader")
    resbody = res.getChild("Envelope").getChild("Body")
    failures = resheader.getChild("failures")
    res_dict = {
        "execution_result": resheader.getChild("desc").getText(),
        "operations": resheader.getChild("oprs").getText(),
        "operation_time": resheader.getChild("oprtime").getText(),
        "consume_quota": resheader.getChild("quota").getText(),
        "remain_quota": resheader.getChild("rquota").getText(),
        "status": resheader.getChild("status").getText(),
    }

    failure_dict = None 
    if failures is not None:
        failure_dict = {
            "code": failures.getChild("code").getText(),
            "message": failures.getChild("message").getText(),
            "position": failures.getChild("position").getText(),
        }
    if resbody is not None:
        res_dict['body']  = resbody
        res_dict['response'] = parse_suds_obj(resbody)


    return res_dict, failure_dict


"""
def dict_to_request(client, acc_key, input):
    if type(input) == type([]):
        output = []
        for e in input:
            output.append(dict_to_request(client, acc_key, e))
        return output
    elif type(input) == type({}):
        request = client.factory.create(acc_key)
        value = input[acc_key.split('.')[-1]]
        request.


    {
        "setTargetInfoRequest":
            {
                'targetInfo' : 
                     {
                         'type' : 2
                         ,'groupId' : 2
                         ,'ktItem' :
                             {
                                 "ktWordList":
                                     [
                                         {
                                             'keyword':'baidu-search'
                                             'pattern':0
                                             'qualification':1
                                         }
                                         {
                                             'keyword':'baidu-search'
                                             'pattern':0
                                             'qualification':1
                                         }
                                     ]
                             }
                         ,'ktItem' : None
                         ,'vtItem' : None
                     }
            }
    }

    
    targetInfo = client.factory.create('setTargetInfoRequest.targetInfo')
    targetInfo.type = 2
    targetInfo.groupId = 228
    ktItem = client.factory.create('setTargetInfoRequest.targetInfo.ktItem')
    ktItem.aliveDays = 30
    ktItem.targetType = 7
    ktWordList1 = client.factory.create('setTargetInfoRequest.targetInfo.ktItem.ktWordList')
    ktWordList1.keyword = 'baidu-search'
    ktWordList1.pattern = 0
    ktWordList1.qualification = 1
    ktWordList2 = client.factory.create('setTargetInfoRequest.targetInfo.ktItem.ktWordList')
    ktWordList2.keyword = 'baidu-union'
    ktWordList2.pattern = 1
    ktWordList2.qualification = 3
    ktItem.ktWordList = []
    ktItem.ktWordList.append(ktWordList1)
    ktItem.ktWordList.append(ktWordList2)
    targetInfo.ktItem = ktItem
    targetInfo.rtItem = None
    targetInfo.vtItem = None
    request.targetInfo = targetInfo

    return request
"""
