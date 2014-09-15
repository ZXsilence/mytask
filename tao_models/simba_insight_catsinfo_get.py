#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: liumingchao
@contact: liumingchao@maimiaotech.com
@date: 2014-08-29 15:47
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import math
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

from TaobaoSdk import  SimbaInsightCatsinfoGetRequest 
from tao_models.common.decorator import  tao_api_exception
from api_server.services.api_service import ApiService
from api_server.common.util import change_obj_to_dict_deeply

'''type=0 获取所有顶级类目信息，第二个参数可以忽略;type=1获取给定类目id所有子类目的详细信息'''
class  SimbaInsightCatsinfoGet(object):
    
    @classmethod
    @tao_api_exception()
    def get_cats_info(cls,t_type,cat_id_list):
        req = SimbaInsightCatsinfoGetRequest()
        req.type=t_type
        req.category_id_list = ','.join([str(item) for item in cat_id_list])
        nick = None
        soft_code = None
        rsp = ApiService.execute(req,nick,soft_code)
        return change_obj_to_dict_deeply(rsp.category_info_list)
    
    @classmethod
    def get_all_cats_info(cls, cat_id_list=[]):
        type = 2
        if len(cat_id_list) == 0:
            type = 0
        first_cat_list = cls.get_cats_info(type, cat_id_list)
        first_cat_ids = [cat['cat_id'] for cat in first_cat_list]
        page_num = int(math.ceil(len(first_cat_ids) / 20.0))
        for i in range(page_num):    
            first_cat_list.extend(cls.get_all_cats_info(first_cat_ids[i*20: i*20+20]))

        return first_cat_list

if __name__ == '__main__':
    cat_list = SimbaInsightCatsinfoGet.get_all_cats_info()
    for cat in cat_list:
        print '%d: %s' % (cat['cat_id'], cat['cat_name'])
