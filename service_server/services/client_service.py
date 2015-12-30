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
            pass
            #raise ErrorResponseException(code=rsp_obj.code, msg=rsp_obj.msg, sub_code=rsp_obj.sub_code, sub_msg=rsp_obj.sub_msg,params=params_dict,rsp=rsp_obj)
        return rsp_obj 

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
        return rsp_dict
