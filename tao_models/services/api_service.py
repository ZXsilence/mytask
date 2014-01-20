#encoding=utf8
"""doc string for module"""
__author__ = 'lym liyangmin@maimiaotech.com'

import sys
import os
import logging
from datetime import datetime

from shop_db.services.shop_info_service import ShopInfoService
from tao_models.common.exceptions import  InvalidAccessTokenException,ApiSourceError
from tao_models.db_models.api_record import ApiRecord
from tao_models.conf.settings import APP_SETTINGS,SERVER_URL,API_NEED_SUBWAY_TOKEN,API_SOURCE,api_source
from TaobaoSdk.Exceptions import ErrorResponseException
from TaobaoSdk import  TaobaoClient

logger = logging.getLogger(__name__)

class ApiService(object):

    #      ==== 共有三种API调用类型 =====
    #    1、API调用和用户有关，如加词，查余额等等
    #    2、API调用和用户无关，如宝贝查询等
    #    3、API调用和软件有关，必须强制指定soft_code,如订单查询、优惠链接等

    @staticmethod
    def execute(req,nick=None,soft_code=None):
        if not nick and not soft_code:
            shop_infos = ShopInfoService.get_shop_infos_by_num(10)
        else:
            session_expired = False
            shop_infos = ShopInfoService.get_shop_infos(nick,soft_code,False)
        return ApiService.execute_with_shop_infos(req,shop_infos)

    @staticmethod
    def execute_with_shop_infos(req,shop_infos):
        #循环shop_infos调用的理由，处理下面的特殊情况：
        #一个用户订购多款软件，shop_info_list的session_expired全为False，但是其中一个订购已退款或失效
        for shop_info in shop_infos:
            soft_code = shop_info['soft_code']
            sid = int(shop_info['sid'])
            app_key = APP_SETTINGS[soft_code]['app_key']
            app_secret = APP_SETTINGS[soft_code]['app_secret']
            access_token = shop_info['access_token']
            api_method = req.method
            if api_method in API_NEED_SUBWAY_TOKEN:
                subway_token = shop_info['subway_token']
                req.subway_token = subway_token
            taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
            rsp = taobao_client.execute(req, access_token)[0]
            #记录API调用
            ApiRecordService.mark_record(req,rsp)
            if rsp.code == 27:
                #错误码27即是InvalidAccessToken,跳过，用其他shop_info进行调用
                ShopInfoService.update_shop_info(soft_code,sid,{'session_expired':True})
                continue
            if not rsp.isSuccess():
                raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg,req=req,rsp=rsp)
            else:
                return rsp
        #查不到有效的shop_info，或者所有调用均为错误码27，扔出过期异常InvalidAccessTokenException
        raise InvalidAccessTokenException

class ApiRecordService(object):

    @staticmethod
    def inc_success_record(source,method):
        today = datetime.today()
        today_str = datetime.strftime(today , '%Y-%m-%d')
        record = ApiRecord.find_api_record(today_str,source,method)
        if not record:
            record_new = {'date':today_str,'source':source,'method':method}
            record_new['success_times'] = 1
            record_new['fail_times'] = 0
            record_new['total_times'] = 1
            ApiRecord.insert_record(record_new)
        else:
            ApiRecord.inc_success_record(today_str,source,method)

    @staticmethod
    def inc_fail_record(source,method):
        today = datetime.today()
        today_str = datetime.strftime(today , '%Y-%m-%d')
        record = ApiRecord.find_api_record(today_str,source,method)
        if not record:
            record_new = {'date':today_str,'source':source,'method':method}
            record_new['success_times'] = 0
            record_new['fail_times'] = 1
            record_new['total_times'] = 1
            ApiRecord.insert_record(record_new)
        else:
            ApiRecord.inc_fail_record(today_str,source,method)

    @staticmethod
    def get_record(date_str,source,method):
        return ApiRecord.find_api_record(date_str,source,method)

    @staticmethod
    def mark_record(req,rsp):
        source = api_source
        if not source or source not in API_SOURCE:
            raise ApiSourceError(source)
        method = req.method
        if rsp.isSuccess():
            ApiRecordService.inc_success_record(source,method)
        #无需记录的错误:  流控，isp错误等
        elif rsp.sub_code and (rsp.sub_code.startswith('isp.') \
                or rsp.sub_code == 'accesscontrol.limited-by-api-access-count'):
            pass
        else:
            ApiRecordService.inc_fail_record(source,method)
        

