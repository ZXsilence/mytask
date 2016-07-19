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
    
    @classmethod
    def get_all_cats(cls):
        cat_list = []
        #get first level cat, ready to traverse all cats 
        cat_queue_list = cls.get_cats_info(0, [])
        
        loop_count = 0

        while len(cat_queue_list) > 0:
            cut_len = min(len(cat_queue_list), 20)

            temp_cat_list = cat_queue_list[:cut_len]
            cat_queue_list = cat_queue_list[cut_len:]

            cat_id_list = []

            for i in range(0, cut_len):
                cat_id_list.append(temp_cat_list[i]["cat_id"])
            
            child_cat_list = cls.get_cats_info(2, cat_id_list)
            
            # shows cat has child ro not
            leaf_flag_list = [True for i in range(0, cut_len)]
            
            for child in child_cat_list:
                parent_id = child["parent_cat_id"]
                leaf_flag_list[cat_id_list.index(parent_id)] = False
            
            for i in range(0, cut_len):
                if leaf_flag_list[i]:
                    temp_cat_list[i]["isLeaf"] = 1
                else:
                    temp_cat_list[i]["isLeaf"] = 0
            
            cat_list.extend(temp_cat_list)
            cat_queue_list.extend(child_cat_list)
            loop_count +=1
            if loop_count >= 20:
                break

        return cat_list
        
if __name__ == '__main__':
    '''cat_list = SimbaInsightCatsinfoGet.get_all_cats_info()
    for cat in cat_list:
        print '%d: %s' % (cat['cat_id'], cat['cat_name'])'''
    
    cat_list = SimbaInsightCatsinfoGet.get_cats_info(2, ["124082001"])
    print cat_list
    #for cat in cat_list:                               
        #print '%d: %s %d' % (cat['cat_id'], cat['cat_name'], cat['cat_level']) 

    '''cat_list = SimbaInsightCatsinfoGet.get_all_cats()
    for cat in cat_list:
        print "%d\t%s\t%d\t%d\t%d" % (cat["cat_id"], cat["cat_name"], cat["cat_level"],cat["parent_cat_id"], cat["isLeaf"])'''
