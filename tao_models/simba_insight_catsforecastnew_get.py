#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2014-08-29 15:28
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

from TaobaoSdk import  SimbaInsightCatsforecastnewGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

class  SimbaInsightCatsforecastnew(object):
    
    @classmethod
    @tao_api_exception()
    def get_words_forecast_cats(cls,words_list):
        req = SimbaInsightCatsforecastnewGetRequest()
        req.bidword_list = ','.join(words_list)
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.category_forecast_list)
    
    @classmethod
    def get_words_forecast_cats_list(cls,words_list):
        cast_info_list = SimbaInsightCatsforecastnew.get_words_forecast_cats(words_list)
        cats_list = []
        for item in cast_info_list:
            import pdb;pdb.set_trace()
            cat_path_id = item.get('cat_path_id',None)
            if not cat_path_id:
                continue
            cat_id = cat_path_id.split(' ')[-1]
            cats_list.append(cat_id)
        return cats_list
            
    @classmethod
    def get_words_forecast_cats_info(cls,words_list):
        cast_info_list = SimbaInsightCatsforecastnew.get_words_forecast_cats(words_list)
        import pdb;pdb.set_trace()
        cats_list = []
        for item in cast_info_list:
            cat_path_id = item.get('cat_path_id',None)
            cat_path_name = item.get('cat_path_name',None)
            if not cat_path_id or not cat_path_name:
                continue
            cat_id = cat_path_id.split(' ')[-1]
            cat_name = cat_path_name.split('>')[-1]
            cats_list.append({'cat_id':cat_id,'cat_name':cat_name,'score':item['score']})
        return cats_list

if __name__ == '__main__':
    words_list = ["连衣裙"]
    res =  SimbaInsightCatsforecastnew.get_words_forecast_cats_info(words_list) 
    for item in res:
        print item,item['cat_name']


