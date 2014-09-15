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

class  SimbaInsightCatsforecastnewGet(object):
    Max_Words = 10 
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
        cats_info_list = []
        while  words_list:
            sub_words_list =words_list[:cls.Max_Words]
            words_list = words_list[cls.Max_Words:]
            cat_sub_list = SimbaInsightCatsforecastnewGet.get_words_forecast_cats(sub_words_list)
            cats_info_list.extend(cat_sub_list)
        all_cats_list = []
        all_score_list = []
        length = len(cats_info_list)
        cats_list = []
        score_list = []
        index = 0 
        for item in cats_info_list:
            cat_path_id = item['cat_path_id']
            cat_id = cat_path_id.split(' ')[-1]
            '''处理连续2个词重复的逻辑'''
            if cat_id not in cats_list:
                cats_list.append(cat_id)
                score_list.append(item['score'])
            else:
                all_cats_list.append(cats_list)
                all_score_list.append(score_list)
                cats_list = []
                score_list = []
                cats_list.append(cat_id)
                score_list.append(item['score'])
                if index == length-1 or cats_info_list[index]['bidword'] !=\
                       cats_info_list[index+1]['bidword'] : 
                    all_cats_list.append(cats_list)
                    all_score_list.append(score_list)
                    cats_list = []
                    score_list = []
                index = index +1
                continue
            if  index == length-1  or  cats_info_list[index]['bidword'] != \
                    cats_info_list[index+1]['bidword']:
                all_cats_list.append(cats_list)
                all_score_list.append(score_list)
                cats_list = []
                score_list = []
            index = index +1
        return all_cats_list,all_score_list
            
    @classmethod
    def get_words_forecast_cats_info(cls,words_list):
        cats_info_list = SimbaInsightCatsforecastnewGet.get_words_forecast_cats(words_list)
        cats_list = []
        for item in cats_info_list:
            cat_path_id = item.get('cat_path_id',None)
            cat_path_name = item.get('cat_path_name',None)
            if not cat_path_id or not cat_path_name:
                continue
            cat_id = cat_path_id.split(' ')[-1]
            cat_name = cat_path_name.split('>')[-1]
            cats_list.append({'cat_id':cat_id,'cat_name':cat_name,'score':item['score']})
        return cats_list

if __name__ == '__main__':
    words_list = [u'nt01pro',  u'u12s', u'u12s', u'b81l', u'连衣裙']
    words_list = [u'nt01pro',  u'u12s', u'u12s', u'b81l']
    words_list = [u'nt01pro']
    res,res1 =  SimbaInsightCatsforecastnewGet.get_words_forecast_cats_list(words_list) 
    for item in  res:
        if  len(item) == 1 and  item[0]== u'':
            print "no cat"

