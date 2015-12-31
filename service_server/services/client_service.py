#encoding=utf8
import re
import os
import sys
import logging
import time
import simplejson
from datetime import datetime
from TaobaoSdk.Exceptions import ErrorResponseException
from service_server.conf.settings import API_THRIFT
from service_server.thrift.client_py import JavaApiClient
from api_server.common.decorator import sdk_exception

logger = logging.getLogger(__name__)

class ClientService(object):

    @staticmethod
    def execute(params_dict,nick):
        params_str = simplejson.dumps(params_dict)
        #调用sdk
        rsp_obj = ClientService.query_rpts(params_str,nick)
        if not rsp_obj.get('success'):
            raise ServerEerror(code = rsp_obj.get('code'),msg = rsp_obj.get('msg'))
        return rsp_obj['data']

    @staticmethod
    @sdk_exception(6)
    def query_rpts(params_str,nick):
        #sdk调用函数，有重试机制
        api_client = JavaApiClient(API_THRIFT['host'],API_THRIFT['port'])
        rsp_str = api_client.query_rpts(nick,params_str)
        rsp_dict = simplejson.loads(rsp_str)
        rsp_obj = ClientService.getResponseObj(rsp_dict)
        return rsp_obj

    @staticmethod
    def getResponseObj(rsp_dict):

        return change_obj_to_dict_deeply(rsp_dict)

def change_obj_to_dict_deeply(obj):
    if type(obj) == type([]):
        #列表转换
        return [change_obj_to_dict_deeply(sub_obj) for sub_obj in obj]
    elif type(obj) == type({}):
        if len(obj) == 9 and len(set(obj.keys()) & set(['seconds','year','month','hours','time','date','minutes','day','timezoneOffset'])) == 9:
            return datetime.fromtimestamp(obj['time']/1000)
        else:
            return dict((k,change_obj_to_dict_deeply(v)) for k,v in obj.iteritems())
    else:
        #基本类型，无需转换
        return obj
