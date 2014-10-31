#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-07-17 17:32
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""

import sys
import os
import json
import datetime as dt
import logging

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from datetime import datetime
from TaobaoSdk import WangwangEserviceReceivenumGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply 

logger = logging.getLogger(__name__)


class WangwangEserviceReceivenumGet(object):

    @classmethod
    def get_receivenum_list(cls,nick,serivce_nick_list,start_date,end_date):
        temp_date = datetime.combine(start_date.date(),start_date.time())
        data_list = []
        while temp_date <= end_date:
            l = cls._get_receivenum_list(nick,serivce_nick_list,temp_date,temp_date)
            data_list.extend(l)
            temp_date += dt.timedelta(1)
        return data_list

    @classmethod
    def _get_receivenum_list(cls,nick,serivce_nick_list,start_date,end_date):
        page_size = 30
        page_count = (len(serivce_nick_list) -1)/page_size +1
        temp_date = datetime.combine(start_date.date(),start_date.time())
        soft_code = None
        data_list = []
        for page_no in range(page_count):
            req = WangwangEserviceReceivenumGetRequest() 
            tem_nick_list = serivce_nick_list[page_no*page_size:(page_no + 1)*page_size]
            req.service_staff_id = ','.join(tem_nick_list)
            req.start_date = start_date.strftime('%Y-%m-%d')
            req.end_date = end_date.strftime('%Y-%m-%d')
            rsp = ApiService.execute(req,nick,soft_code)
            temp_list = change_obj_to_dict_deeply(rsp.reply_stat_list_on_days)
            real_dict = {}
            for obj in temp_list:
                reply_date = obj['reply_stat_on_day']['reply_date']
                real_dict[reply_date] = obj
            data_list.extend(real_dict.values())
        return data_list

if __name__ == "__main__":
    nick = "麦苗科技"
    serivce_nick_list = ['cntaobao麦苗科技:茂茂','cntaobao麦苗科技']
    start_date = datetime(2014,8,13)
    end_date = datetime(2014,8,14)
    activity_list = WangwangEserviceReceivenumGet.get_receivenum_list(nick,serivce_nick_list,start_date,end_date)
    print '============'
    print activity_list
