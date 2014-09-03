#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2014-08-29 15:58
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

from TaobaoSdk import  SimbaInsightCatstopwordnewGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class SimbaInsightCatstopwordnewGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_cats_top_words(cls,cat_id,sdate,edate,dimension,page_size=20):
        req = SimbaInsightCatstopwordnewGetRequest()
        req.cat_id=cat_id
        req.start_date = sdate.strftime("%Y-%m-%d")
        req.end_date = edate.strftime("%Y-%m-%d")
        req.page_size = page_size
        req.dimension = dimension
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.topword_data_list)

if __name__ == '__main__':
   edate = datetime.datetime.now() - datetime.timedelta(days = 1)
   sdate = edate - datetime.timedelta(days = 7)
   dimension = "click"
   cat_id = 50023582
   words =  SimbaInsightCatstopwordnewGet.get_cats_top_words(cat_id,sdate,edate,dimension)


