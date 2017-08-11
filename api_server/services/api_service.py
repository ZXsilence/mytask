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
from api_server.services.api_cache_service import ApiCacheService
from api_server.services.api_cache_config import ApiCacheConfig
from api_server.services.api_virtual_service import ApiVirtualService
from api_server.services.api_virtual_replace_key_config import ApiVirtualReplaceKeyConfig
from api_server.services.subClass.exceptions import ApiVirtualResponseException

logger = logging.getLogger(__name__)
logger2 = logging.getLogger("api_virtual")

class ApiService(object):

    @staticmethod
    def execute(req,nick=None,soft_code=None,cache = True):
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
        if not params_dict.get('nick') and nick:
            params_dict['nick'] = nick
        method_config = ApiCacheConfig.API_METHOD_CONFIG.get(params_dict['method'])

        api_name = params_dict['method']
        replace_api_names = ApiVirtualReplaceKeyConfig.API_OUTPUT_REPLACE_KEY.keys()
        API_VIRTUAL = api_name in replace_api_names

        is_get = True
        cache_key = None
        #北斗临时单独处理
        if 'bd_webpage' == api_source:
            cache = False
        if cache and method_config:
            is_get = method_config.get('is_get',False)
            cache_key = ApiCacheService.get_cache_key(params_dict)
        if cache and is_get and cache_key:
            cache_data = ApiCacheService.get_cache(cache_key,params_dict)
            if cache_data:
                rsp_obj = ApiService.getResponseObj(cache_data)
                if 'sub_code' not in rsp_obj.responseBody and  'sub_msg' not in rsp_obj.responseBody:
                    return rsp_obj

        ApiVirtualService_obj = None
        if API_VIRTUAL:
            ApiVirtualService_obj = ApiVirtualService(params_dict,soft_code,api_source)
            rsp_dict = ApiVirtualService_obj.call_virtual_db()
            if not rsp_dict:
                msg = "错误：测试模式，call_virtual_db返回为None！"
                logger2.error(msg)
                raise ErrorResponseException(code=100, msg=msg, sub_msg=msg)
        else:
            rsp_dict = ApiService.call_sdk(params_str,nick,soft_code,api_source)
        rsp_obj = ApiService.getResponseObj(rsp_dict,ApiVirtualService_obj,API_VIRTUAL)
        if not rsp_obj.isSuccess() or ('sub_code' in rsp_obj.responseBody and 'sub_msg' in rsp_obj.responseBody):
            raise ErrorResponseException(code=rsp_obj.code, msg=rsp_obj.msg, sub_code=rsp_obj.sub_code, sub_msg=rsp_obj.sub_msg,params=params_dict,rsp=rsp_obj)
        #update清理cache
        if cache and method_config:
            if is_get and cache_key:
                ApiCacheService.set_cache(cache_key,rsp_dict,{'nick':nick or params_dict.get('nick'),'cache_name':method_config['cache_name']},params_dict)
            elif not is_get:
                ApiCacheService.clear_cache(nick or params_dict.get('nick'),params_dict)
        return rsp_obj 

    @staticmethod
    @sdk_exception(5)
    def call_sdk(params_str,nick,soft_code,api_source):
        #sdk调用函数，有重试机制
        api_client = ApiCenterClient(API_THRIFT['host'],API_THRIFT['port'])
        rsp_str = api_client.execute(params_str,nick,soft_code,api_source)
        rsp_dict = simplejson.loads(rsp_str)
        return rsp_dict

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
    def getResponseObj(rsp_dict,ApiVirtualService_obj=None,API_VIRTUAL=None):
        '''
        将rsp_dict转为rsp_obj
        '''
        if API_VIRTUAL and not ApiVirtualService_obj:
            msg = "错误：测试模式，ApiVirtualService_obj对象为空，不能走虚拟库！"
            logger2.error(msg)
            raise ErrorResponseException(code=100, msg=msg, sub_msg=msg)

        responses = list()
        rawContent = simplejson.dumps(rsp_dict)
        try:
            for key, value in rsp_dict.iteritems():
                key = str().join([x.capitalize() for x in key.split("_")])
                ResponseClass = getattr(sys.modules["TaobaoSdk.Response.%s" % key], key)
                response = ResponseClass(value)
                response.responseStatus = 200
                if API_VIRTUAL:
                    try:
                        response,rawContent = ApiVirtualService_obj.replace_virtual_response(response)
                        if not response or not rawContent:
                            msg = "替换返回值失败！"
                            raise ApiVirtualResponseException(msg)
                    except Exception,e:
                        logger.error(e.msg)
                        raise e
                response.responseBody = rawContent
                responses.append(response)
            return (tuple(responses))[0]
        except ApiVirtualResponseException,e:
            raise e
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

    @staticmethod
    def get_app_settings_by_appkey(appkey):
        for soft_code,app_settings in APP_SETTINGS.iteritems():
            if appkey == app_settings['app_key']:
                return app_settings
        return {}


