#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2013-09-23 14:09
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import logging
import logging.config
import datetime as dt
from datetime import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import FuwuScoresGetRequest 
from TaobaoSdk import TaobaoClient
from TaobaoSdk.Exceptions.ErrorResponseException import ErrorResponseException
from tao_models.common.decorator import  tao_api_exception
from api_server.conf.settings import APP_SETTINGS,SERVER_URL,API_HOST,API_PORT
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

logger = logging.getLogger(__name__)

class FuwuScoresGet(object):
    """应用评价"""
    PAGE_SIZE = 100

    @classmethod
    def get_fuwu_scores_by_apicenter(cls,date_time,soft_code,page_no=1):
        result_list = []
        req = FuwuScoresGetRequest()
        req.current_page = page_no
        req.date = date_time
        req.page_size = 100
        nick = None
        rsp = ApiService.execute(req,nick,soft_code)
        result_list = change_obj_to_dict_deeply(rsp.score_result)
        if result_list is None:
            result_list = []
        return result_list

    @classmethod
    @tao_api_exception(15)
    def sub_get_fuwu_scores(cls,req,soft_code):
        nick = None
        rsp = ApiService.execute(req,nick,soft_code)
        return rsp.score_result

    @classmethod
    @tao_api_exception(15)
    def get_fuwu_scores(cls,date_time,soft_code,page_no = 1):
        app_key = APP_SETTINGS[soft_code]['app_key']
        app_secret = APP_SETTINGS[soft_code]['app_secret']

        req = FuwuScoresGetRequest()
        req.current_page = page_no
        req.date = date_time.strftime('%Y-%m-%d') if type(date_time) == type(datetime.now()) else date_time
        req.page_size = 100
        params = ApiService.getReqParameters(req)
        taobao_client = TaobaoClient(SERVER_URL,app_key,app_secret)
        rsp = ApiService.getResponseObj(taobao_client.execute(params, ''))
        if not rsp.isSuccess():
            raise ErrorResponseException(code=rsp.code, msg=rsp.msg, sub_code=rsp.sub_code, sub_msg=rsp.sub_msg)
        result_list = change_obj_to_dict_deeply(rsp.score_result)
        if result_list is None:
            result_list = []
        return result_list

    @classmethod
    def get_all_fuwu_scores(cls,date_time,soft_code):
        """获取所有评价"""

        page_no = 1
        data_list = []
        flag = True
        while flag:
            page_data = cls.get_fuwu_scores(date_time,soft_code,page_no)
            if not page_data or len(page_data) < cls.PAGE_SIZE:
                flag = False
            page_no += 1
            if page_data:
                data_list.extend(page_data)
        return data_list

            
if __name__ == "__main__":
    d = datetime.combine(datetime.today(),dt.time()) - dt.timedelta(3)
    d = datetime.now()
    soft_code = 'BD'
    #print FuwuScoresGet.get_fuwu_scores(d,soft_code)
    i = 0
    while (i < 20):
        i += 1
        try:
            suggest_list = FuwuScoresGet.get_all_fuwu_scores('2015-02-04','BD')
            print len(suggest_list)
        except Exception,e:
            print 'error:%s' %i
            print e
            continue

        print i 

