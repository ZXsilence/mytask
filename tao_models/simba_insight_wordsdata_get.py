#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2014-08-29 14:46
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

from TaobaoSdk import SimbaInsightWordsdataGetRequest
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class  SimbaInsightWordsdataGet(object):
    Max_Words = 100
    @classmethod
    @tao_api_exception()
    def _get_words_data(cls,words_list,sdate,edate):
        req = SimbaInsightWordsdataGetRequest()
        req.bidword_list = ','.join(words_list)
        req.start_date = sdate.strftime("%Y-%m-%d")
        req.end_date = edate.strftime("%Y-%m-%d")
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.word_data_list)
    
    @classmethod
    def get_words_data(cls,words_list,sdate,edate):
        total_list = []
        while words_list:
            sub_word_list = words_list[:cls.Max_Words]
            sub_list = SimbaInsightWordsdataGet._get_words_data(sub_word_list,sdate,edate)
            words_list = words_list[cls.Max_Words:]
            total_list.extend(sub_list)
        return total_list




if __name__ == '__main__':
    impression = 0
    cost = 0
    from  pymongo import Connection
    con=Connection(host='localhost',port=2201)
    col=con['suggest_db']['suggest_word']
    cur = col.find().limit(100)
    words_list = []
    for item in cur[:100]:
        words_list.append(item['_id'])
    edate = datetime.datetime.now() - datetime.timedelta(days = 1)
    sdate = edate - datetime.timedelta(days = 1)
    print sdate ,edate
    res =  SimbaInsightWordsdataGet.get_words_data(words_list,sdate,edate)
    print len(res)
