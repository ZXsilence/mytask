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
import simplejson
from shop_db.services.shop_info_service import ShopInfoService
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_SOURCE,API_THRIFT
from TaobaoSdk import  TaobaoClient
from api_server.services.api_record_service import ApiRecordService
from api_server.conf.settings import logger
   
class ApiCenterHandle(object):

    def execute(self,params,nick,soft_code,api_source):
        """
            params       API请求淘宝的参数
            api_source   API调用源
            nick为空字符串，表示该API请求和用户无关，可取任意有效的access_token
            soft_code为空字符串 ，表示该API请求和APP无关，可任取app_key
        """

        params = simplejson.loads(params)
        method = params['method']
        api_record = ApiRecordService.get_record(api_source,method)
        nick = nick.decode('utf8')
        logger.info('api start , source:%s , method:%s , soft_code:%s , nick:%s , params_nick:%s'\
                %(api_source,method,soft_code,nick,params.get('nick',None)))
        if not api_source or api_source not in API_SOURCE:
            #API调用源检查
            rsp = ApiCenterHandle.get_source_error_rsp(api_source)
            logger.error('api source error, source:%s , method:%s , soft_code:%s , nick:%s , params_nick:%s'\
                    %(api_source,method,soft_code,nick,params.get('nick',None)))
            return simplejson.dumps(rsp)
        if api_record and api_record['all_day_limit']:
            #API全天流控检查
            rsp = ApiCenterHandle.get_call_limit_rsp()
            logger.error('api limit error, source:%s , method:%s , soft_code:%s , nick:%s , params_nick:%s'\
                    %(api_source,method,soft_code,nick,params.get('nick',None)))
            return simplejson.dumps(rsp)

        #根据入参的情况，获取相应的shop_infos列表
        session_expired = False
        if not nick and not soft_code:
            shop_infos = ShopInfoService.get_shop_infos_by_num(10,session_expired)
        else:
            shop_infos = ShopInfoService.get_shop_infos(nick,soft_code,session_expired)
        #根据shop_infos列表调用API
        rsp_dict = ApiCenterHandle.execute_with_shop_infos(params,shop_infos,api_source)

        #调用失败的api需记录详细的调用信息 
        if rsp_dict.has_key('error_response'):
            logger.warning('api exception,source:%s , method:%s , soft_code:%s , nick:%s , params:%s , responseBody:%s'\
                    %(api_source,method,soft_code,nick,params,rsp_dict['error_response']))
        else:
            logger.info('api end , source:%s , method:%s , soft_code:%s , nick:%s , params_nick:%s'\
                            %(api_source,method,soft_code,nick,params.get('nick',None)))

        return simplejson.dumps(rsp_dict)

    @staticmethod
    def execute_with_shop_infos(params,shop_infos,api_source):
        """
            对shop_infos循环调用，避免下面的特殊情况：
            一个用户订购多款软件，shop_info_list的session_expired全为False，但是其中一个订购已退款或失效
        """
        rsp_dict = {}
        invalid_session_count = 0
        call_limit_count = 0
        total_shops_count = len(shop_infos)
        for shop_info in shop_infos:
            soft_code = shop_info['soft_code']
            sid = int(shop_info['sid'])
            nick = shop_info['nick']
            app_key = APP_SETTINGS[soft_code]['app_key']
            app_secret = APP_SETTINGS[soft_code]['app_secret']
            access_token = shop_info['access_token']
            api_method = params['method']

            #报表相关接口需要subway_token
            if api_method in API_NEED_SUBWAY_TOKEN:
                subway_token = shop_info['subway_token']
                params['subway_token'] = subway_token

            #掌中宝的非open平台access_token，需要加上header
            if soft_code == 'QN' and not shop_info.get('is_open_access_token',False): 
                params.update(shop_info.get('header',{}))

            #发送请求
            taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
            rsp_dict = taobao_client.execute(params, access_token)

            #记录API调用
            ApiCenterHandle.mark_record(params,rsp_dict,api_source)

            #异常处理
            if rsp_dict.has_key('error_response') and rsp_dict['error_response'].get('code',0)== 27:
                #错误码27即是InvalidAccessToken,跳过，用其他shop_info进行调用
                ShopInfoService.update_shop_info(soft_code,nick,{'session_expired':True})
                logger.error("Invalid session , source:%s , method : %s , nick:%s , soft_code:%s"%(api_source,api_method,shop_info['nick'],shop_info['soft_code']))
                invalid_session_count += 1
                #切换app_key
                continue
            if rsp_dict.has_key('error_response') and rsp_dict['error_response'].get('code',0)== 7:
                #API全天被限
                wait_seconds = int(rsp_dict['error_response']['sub_msg'].split(' ')[5])
                if wait_seconds > 60:
                    ApiRecordService.set_all_day_limit(api_method,api_source,True)
                    logger.error("API ALL DAY LIMITS , wait_seconds:%s , source:%s , method:%s , nick:%s , soft_code:%s"%(wait_seconds,api_source,api_method,shop_info['nick'],shop_info['soft_code']))
                    call_limit_count += 1
                    #切换app_key
                    continue
            return rsp_dict

        if total_shops_count and call_limit_count == total_shops_count:
            return ApiCenterHandle.get_call_limit_rsp()
        else:
            return ApiCenterHandle.get_invalid_session_rsp()

    @staticmethod
    def mark_record(params,rsp,source):
        method = params['method']
        if not rsp.has_key('error_response'):
            ApiRecordService.inc_success_record(source,method)
        elif rsp['error_response']['sub_code'] and (rsp['error_response']['sub_code'].startswith('isp.') \
                or rsp['error_response']['sub_code'] == 'accesscontrol.limited-by-api-access-count'):
            #无需记录的错误:  流控，isp错误等
            pass
        else:
            ApiRecordService.inc_fail_record(source,method)

    @staticmethod
    def get_invalid_session_rsp():
        rsp = {'error_response':{}}
        rsp['error_response']['code'] = 27
        rsp['error_response']['sub_code'] = 'invalid-shop_info'
        rsp['error_response']['msg'] = 'can not find valid shop_info'
        rsp['error_response']['sub_msg'] = 'can not find valid shop_info'
        return rsp

    @staticmethod
    def get_source_error_rsp(api_source):
        rsp = {'error_response':{}}
        rsp['error_response']['code'] = 1000.1
        rsp['error_response']['msg'] = 'Api Source Error'
        rsp['error_response']['sub_msg'] = 'current api source is %s , error'%api_source
        rsp['error_response']['sub_code'] = 'api-source-error'
        return rsp

    @staticmethod
    def get_call_limit_rsp():
        rsp = {'error_response':{}}
        rsp['error_response']['code'] = 7
        rsp['error_response']['msg'] = 'App Call Limited'
        rsp['error_response']['sub_msg'] = 'This ban will last for 123456 more seconds'
        rsp['error_response']['sub_code'] = 'accesscontrol.limited-by-api-access-count'
        return rsp

    def say(self, msg):
        return "Received:%s"%msg

