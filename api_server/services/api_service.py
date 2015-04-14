#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import re
import os
import sys
import logging
import time
import simplejson
from datetime import datetime
from TaobaoSdk.Exceptions import ErrorResponseException
from api_server.conf.settings import API_THRIFT,APP_SETTINGS
from api_server.common.exceptions import ApiSourceError
from api_server.thrift.ApiCenterClient import ApiCenterClient
from api_server.conf.settings import API_SOURCE
from api_server.conf.settings import get_api_source 
from api_server.common.decorator import sdk_exception

logger = logging.getLogger(__name__)

class ApiService(object):

    @staticmethod
    def execute(req,nick=None,soft_code=None):
        api_source = get_api_source()
        params_dict = ApiService.getReqParameters(req)
        params_str = simplejson.dumps(params_dict)
        if nick is None:
            nick = ''
        if soft_code is None:
            soft_code = ''
        if api_source is None:
            api_source = ''
        #调用sdk
        rsp_obj = ApiService.call_sdk(params_str,nick,soft_code,api_source)
        if not rsp_obj.isSuccess():
            raise ErrorResponseException(code=rsp_obj.code, msg=rsp_obj.msg, sub_code=rsp_obj.sub_code, sub_msg=rsp_obj.sub_msg,params=params_dict,rsp=rsp_obj)
        return rsp_obj 

    @staticmethod
    @sdk_exception(20)
    def call_sdk(params_str,nick,soft_code,api_source):
        #sdk调用函数，有重试机制
        api_client = ApiCenterClient(API_THRIFT['host'],API_THRIFT['port'])
        rsp_str = api_client.execute(params_str,nick,soft_code,api_source)
        rsp_dict = simplejson.loads(rsp_str)
        rsp_obj = ApiService.getResponseObj(rsp_dict)
        return rsp_obj

    @staticmethod
    def getReqParameters(req):
        '''
        将req对象转换为dict
        '''
        parameters = dict()
        for key, value in req.__dict__.iteritems():
            if key == 'timestamp':
                #value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))
                value = str(long(time.time() * 1000))
            if value == None:
                continue
            parameters[key] = unicode(value)
        return parameters

    @staticmethod
    def getResponseObj(rsp_dict):
        '''
        将rsp_dict转为rsp_obj
        '''
        responses = list()
        rawContent = simplejson.dumps(rsp_dict)
        try:
            for key, value in rsp_dict.iteritems():
                key = str().join([x.capitalize() for x in key.split("_")])
                ResponseClass = getattr(sys.modules["TaobaoSdk.Response.%s" % key], key)
                response = ResponseClass(value)
                response.responseStatus = 200
                response.responseBody = rawContent
                responses.append(response)
            return (tuple(responses))[0]
        except ValueError,e:
            if "does not match format '%Y-%m-%d %H:%M:%S'" in str(e):
                #时间转换
                while(re.search('[a-zA-Z\x80-\xff]+\d{3}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}',rawContent)):
                    match_obj = re.search('[a-zA-Z\x80-\xff]+\d{3}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}',rawContent)
                    match_obj2 = re.search('\D\d{3}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}',rawContent)
                    begin = match_obj.start()
                    end = match_obj2.start()+1
                    rawContent = rawContent[:begin] + '2'+ rawContent[end:]
                #重新生成response
                for key, value in rsp_dict.iteritems():
                    key = str().join([x.capitalize() for x in key.split("_")])
                    ResponseClass = getattr(sys.modules["TaobaoSdk.Response.%s" % key], key)
                    response = ResponseClass(value)
                    response.responseStatus = 200
                    response.responseBody = rawContent
                    responses.append(response)
                return (tuple(responses))[0]

    @staticmethod
    def get_app_settings_by_soft_code(soft_code):
        if not APP_SETTINGS.has_key(soft_code):
            return {}
        return APP_SETTINGS[soft_code]

    @staticmethod
    def get_app_settings_by_article_code(article_code):
        for soft_code,app_settings in APP_SETTINGS.iteritems():
            if article_code == app_settings['article_code']:
                return app_settings
        return {}

