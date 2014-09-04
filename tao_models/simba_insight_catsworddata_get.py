#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2014-08-29 17:39
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

from TaobaoSdk import  SimbaInsightCatsworddataGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class SimbaInsightCatsworddataGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_words_cats_data(cls,cat_id,bidword_list,sdate,edate):
        req = SimbaInsightCatsworddataGetRequest()
        req.cat_id=cat_id
        req.bidword_list = ','.join(bidword_list)
        req.start_date = sdate.strftime("%Y-%m-%d")
        req.end_date = edate.strftime("%Y-%m-%d")
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.catword_data_list)

if __name__ == '__main__':
    bidword_list = ["连衣裙"]
    cat_id = 50000852 
    edate = datetime.datetime.now() - datetime.timedelta(days = 1)
    sdate = edate - datetime.timedelta(days = 7)
    print SimbaInsightCatsworddataGet.get_cats_top_words(cat_id,bidword_list,sdate,edate)

