#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2014-09-01 10:24
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""



import sys
import os
import logging
import logging.config
import datetime

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    from api_server.conf import set_env
    set_env.getEnvReady()
    from api_server.conf.settings import set_api_source
    set_api_source('normal_test')

from TaobaoSdk import  SimbaInsightWordspricedataGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class  SimbaInsightWordspricedataGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_words_price_data(cls,bidword,sdate,edate):
        req = SimbaInsightWordspricedataGetRequest()
        req.bidword = bidword
        req.start_date = sdate.strftime("%Y-%m-%d")
        req.end_date = edate.strftime("%Y-%m-%d")
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.word_pricedata_list)

if __name__ == '__main__':
    bidword = "连衣裙"
    edate = datetime.datetime.now() - datetime.timedelta(days = 1)
    sdate = edate - datetime.timedelta(days = 7)
    res =  SimbaInsightWordspricedataGet.get_words_price_data(bidword,sdate,edate)
    for item in res:
        print item
