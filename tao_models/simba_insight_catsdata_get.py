#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2014-08-29 15:17
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

from TaobaoSdk import  SimbaInsightCatsdataGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class  SimbaInsightCatsdataGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_cats_data(cls,cat_id_list,sdate,edate):
        #req = SimbaInsightCatsdataGetRequest()
        #req.category_id_list = ','.join([str(item) for item in cat_id_list])
        #req.start_date = sdate.strftime("%Y-%m-%d")
        #req.end_date = edate.strftime("%Y-%m-%d")
        #nick = None
        #soft_code = None
        #rsp = ApiService.execute(req,nick,soft_code)
        #return change_obj_to_dict_deeply(rsp.cat_data_list)
        return []

if __name__ == '__main__':
   edate = datetime.datetime.now() - datetime.timedelta(days = 1)
   sdate = edate - datetime.timedelta(days = 7)
   cat_id_list = [50023582,50023591]
   print SimbaInsightCatsdataGet.get_cats_data(cat_id_list,sdate,edate)
